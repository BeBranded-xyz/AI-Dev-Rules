"""Hooks execute only synthetic check commands against disposable projects."""

import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class HookTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(prefix='ruleset-hooks-')
        self.addCleanup(self.temporary.cleanup)
        self.project = Path(self.temporary.name)
        (self.project / '.claude').mkdir()
        self.environment = dict(os.environ)
        self.environment.pop('CHECK_COMMAND', None)
        self.environment['CLAUDE_PROJECT_DIR'] = str(self.project)
        self.environment['TMPDIR'] = str(self.project)

    def hook(self, name: str, payload: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ['bash', str(ROOT / 'claude/hooks' / name)], input=payload,
            cwd=self.project, env=self.environment, capture_output=True,
            text=True, timeout=10, check=False,
        )

    def commit(self, command: str = 'git commit -m test') -> subprocess.CompletedProcess[str]:
        return self.hook('pre-commit-check.sh', json.dumps({'tool_input': {'command': command}}))

    def test_missing_or_blank_check_blocks_commit(self) -> None:
        for command in (None, '', '   '):
            with self.subTest(command=command):
                if command is not None:
                    (self.project / '.claude/check-command').write_text(command)
                result = self.commit()
                self.assertEqual(result.returncode, 2)
                self.assertIn('.claude/check-command', result.stderr)

    def test_success_failure_and_private_log_cleanup(self) -> None:
        for command, expected in (('true', 0), ('echo check-failed; false', 2)):
            with self.subTest(command=command):
                self.environment['CHECK_COMMAND'] = command
                result = self.commit()
                self.assertEqual(result.returncode, expected)
                self.assertEqual(list(self.project.glob('claude-check.*')), [])
                if expected:
                    self.assertIn('check-failed', result.stderr)

    def test_precedence_and_make_fallback(self) -> None:
        (self.project / 'Makefile').write_text('check:\n\t@true\n')
        self.assertEqual(self.commit().returncode, 0)
        (self.project / '.claude/check-command').write_text('false\n')
        self.assertEqual(self.commit().returncode, 2)
        self.environment['CHECK_COMMAND'] = 'true'
        self.assertEqual(self.commit().returncode, 0)

    def test_non_commit_does_not_run_check(self) -> None:
        self.environment['CHECK_COMMAND'] = 'touch unexpected; false'
        self.assertEqual(self.commit('git status --short').returncode, 0)
        self.assertFalse((self.project / 'unexpected').exists())

    def test_bypass_flags_and_amend_are_checked(self) -> None:
        self.environment['CHECK_COMMAND'] = 'true'
        for flag in ('--no-verify', '-n'):
            with self.subTest(flag=flag):
                self.assertEqual(self.commit('git commit ' + flag).returncode, 2)
        self.environment['CHECK_COMMAND'] = 'false'
        self.assertEqual(self.commit('git commit --amend').returncode, 2)

    def test_invalid_payload_and_missing_root_block(self) -> None:
        self.assertEqual(self.hook('pre-commit-check.sh', '{').returncode, 2)
        self.environment['CLAUDE_PROJECT_DIR'] = str(self.project / 'missing')
        self.assertEqual(self.commit().returncode, 2)

    def test_env_paths_block_and_placeholder_examples_pass(self) -> None:
        for path, expected in (('.env', 2), ('.env.local', 2), ('.env.example', 0)):
            with self.subTest(path=path):
                result = self.hook('block-secrets.sh', json.dumps({'tool_input': {
                    'file_path': str(self.project / path), 'content': 'TOKEN={{TOKEN}}',
                }}))
                self.assertEqual(result.returncode, expected)

    def test_secret_patterns_cover_all_edit_shapes_and_file_types(self) -> None:
        secret = 'sk_live_' + 'A' * 24  # Synthetic, never an actual credential.
        shapes = ({'content': secret}, {'new_string': secret},
                  {'edits': [{'new_string': 'safe'}, {'new_string': secret}]})
        for path in ('app.ts', 'README.md', '.env.example', 'fixtures/data.txt'):
            for shape in shapes:
                with self.subTest(path=path, shape=list(shape)):
                    payload = {'tool_input': {'file_path': str(self.project / path), **shape}}
                    result = self.hook('block-secrets.sh', json.dumps(payload))
                    self.assertEqual(result.returncode, 2)
                    self.assertNotIn(secret, result.stderr)

    def test_secret_parser_failures_block(self) -> None:
        for payload in ('{', '{}', '{"tool_input": {"file_path": "x", "content": 42}}'):
            with self.subTest(payload=payload):
                self.assertEqual(self.hook('block-secrets.sh', payload).returncode, 2)

    def test_safe_code_passes(self) -> None:
        payload = {'tool_input': {'file_path': str(self.project / 'app.ts'),
                                  'content': 'const token = config.apiToken;'}}
        self.assertEqual(self.hook('block-secrets.sh', json.dumps(payload)).returncode, 0)
