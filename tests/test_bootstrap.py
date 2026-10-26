"""Exercise the actual installer in disposable directories; no external services."""

from pathlib import Path
import re
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class BootstrapTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(prefix='ruleset-test-')
        self.addCleanup(self.temporary.cleanup)
        self.destination = Path(self.temporary.name) / 'project with spaces'

    def install(self, target: str = 'both', *options: str) -> str:
        result = subprocess.run(
            ['bash', str(ROOT / 'init.sh'), '--dest', str(self.destination),
             '--target', target, '--name', 'Fixture Project', *options],
            capture_output=True, text=True, timeout=60, check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        return result.stdout

    def snapshot(self) -> dict[str, bytes]:
        return {
            str(p.relative_to(self.destination)): p.read_bytes()
            for p in self.destination.rglob('*') if p.is_file()
            and p.name != '.ruleset-version'  # Contains the wall-clock date.
        }

    def test_both_targets_preserve_bodies_and_activation(self) -> None:
        self.install()
        for folder in ('core', 'languages', 'platforms', 'modules'):
            for source in (ROOT / folder).glob('*.mdc'):
                with self.subTest(rule=str(source)):
                    self.assert_rule_conversion(source)
        self.assertIn('Fixture Project', (self.destination / 'PROJECT.md').read_text())
        self.assertTrue((self.destination / '.ruleset-version').is_file())
        self.assertEqual((self.destination / 'docs/reference/ruleset-changelog.md').read_bytes(),
                         (ROOT / 'CHANGELOG.md').read_bytes())

    def assert_rule_conversion(self, source: Path) -> None:
        relative = source.relative_to(ROOT)
        original = source.read_text(encoding='utf-8')
        cursor = self.destination / '.cursor/rules' / relative
        self.assertEqual(cursor.read_text(encoding='utf-8'), original)
        _, metadata, body = original.split('---\n', 2)
        always = 'alwaysApply: true' in metadata
        patterns = re.findall(r'^  - "([^"]+)"$', metadata, re.M)
        on_demand = not always and not patterns
        directory = 'rules-on-demand' if on_demand else 'rules'
        converted = Path('.claude') / directory / relative.with_suffix('.md')
        output = (self.destination / converted).read_text(encoding='utf-8')
        _, header, converted_body = output.split('---\n', 2)
        self.assertEqual(converted_body, body)
        self.assertNotIn('globs:', header)
        self.assertNotIn('alwaysApply:', header)
        self.assertEqual(re.findall(r'^  - "([^"]+)"$', header, re.M),
                         [] if always else patterns)
        if on_demand:
            self.assertIn('@' + str(converted),
                          (self.destination / 'CLAUDE.md').read_text())

    def test_single_targets_do_not_install_other_harness(self) -> None:
        for target, other in (('cursor', '.claude'), ('claude', '.cursor')):
            with self.subTest(target=target):
                self.destination = Path(self.temporary.name) / target
                self.install(target)
                self.assertFalse((self.destination / other).exists())
                self.assertTrue((self.destination / 'TEST_PLAN.md').is_file())

    def test_ruleset_version_does_not_leak_local_paths_or_credentials(self) -> None:
        self.install()
        recorded = (self.destination / '.ruleset-version').read_text(encoding='utf-8')
        self.assertNotIn(str(ROOT), recorded)
        self.assertNotIn(str(Path.home()), recorded)
        source = re.search(r'^source=(.*)$', recorded, re.M).group(1)
        self.assertNotRegex(source, r'://[^/@]+@', 'credentials in the source URL')
        self.assertFalse(source.startswith('/'), source)

    def assert_agents_index(self, root: str) -> str:
        agents = (self.destination / 'AGENTS.md').read_text(encoding='utf-8')
        self.assertIn('Fixture Project', agents)
        self.assertNotIn('{{PROJECT_NAME}}', agents)
        self.assertNotIn('{{RULES_ROOT}}', agents)
        self.assertEqual(agents.count('## Rule files'), 1)
        listed = re.findall(r'^- `([^`]+\.md)`', agents, re.M)
        installed = sorted(
            p.relative_to(self.destination).as_posix()
            for folder in ('rules', 'rules-on-demand')
            for p in (self.destination / root / folder).rglob('*.md')
        )
        self.assertEqual(sorted(listed), installed)
        self.assertIn(f'`{root}/rules/core/ai-workflow.md`', agents)
        return agents

    def test_codex_alone_installs_rules_and_skills_under_agents(self) -> None:
        self.install('codex')
        self.assert_agents_index('.agents')
        self.assertTrue((self.destination / '.agents/skills/check/SKILL.md').is_file())
        for absent in ('.claude', '.cursor', 'CLAUDE.md'):
            self.assertFalse((self.destination / absent).exists(), absent)
        self.assertTrue((self.destination / 'PROJECT.md').is_file())

    def test_codex_with_claude_reuses_claude_rules(self) -> None:
        self.install('claude,codex', '--check', 'make check')
        agents = self.assert_agents_index('.claude')
        self.assertIn('Check command: `make check`', agents)
        self.assertNotIn('{{', agents)
        self.assertIn('.claude/skills/*/SKILL.md', agents)
        self.assertFalse((self.destination / '.agents').exists())
        self.assertFalse((self.destination / '.cursor').exists())
        self.assertTrue((self.destination / 'CLAUDE.md').is_file())

    def test_all_installs_every_harness(self) -> None:
        self.install('all')
        self.assert_agents_index('.claude')
        for present in ('.cursor/rules/core/security.mdc', '.claude/settings.json', 'CLAUDE.md'):
            self.assertTrue((self.destination / present).exists(), present)

    def test_update_keeps_agents_text_and_rebuilds_index(self) -> None:
        self.install('claude,codex')
        agents = self.destination / 'AGENTS.md'
        agents.write_text('Custom agent instructions\n\n' + agents.read_text())
        stale = self.destination / '.claude/rules/modules/removed-upstream.md'
        stale.write_text('---\ndescription: Stale\n---\nStale rule\n')
        self.install('claude,codex', '--update')
        self.assertTrue(agents.read_text().startswith('Custom agent instructions\n'))
        self.assertFalse(stale.exists())
        self.assertNotIn('removed-upstream', agents.read_text())
        self.assert_agents_index('.claude')

    def test_target_lists_are_validated(self) -> None:
        for target in ('claude,foo', 'claude,', ',codex', 'claude,,codex', 'codex cursor'):
            with self.subTest(target=target):
                destination = Path(self.temporary.name) / 'invalid-list'
                result = subprocess.run(
                    ['bash', str(ROOT / 'init.sh'), '--dest', str(destination),
                     '--target', target], capture_output=True, text=True,
                    timeout=10, check=False,
                )
                self.assertNotEqual(result.returncode, 0)
                self.assertIn('--target must be', result.stderr)
                self.assertFalse(destination.exists())

    def test_reinstall_is_idempotent(self) -> None:
        for target in ('both', 'all', 'codex'):
            with self.subTest(target=target):
                self.destination = Path(self.temporary.name) / f'idempotent-{target}'
                self.install(target)
                before = self.snapshot()
                self.install(target)
                self.assertEqual(self.snapshot(), before)

    def test_update_preserves_customizations_and_refreshes_owned_files(self) -> None:
        self.install()
        protected = ('PROJECT.md', 'TEST_PLAN.md', 'BACKLOG.md', '.env.example',
                     'docs/RUNBOOK.md', '.claude/settings.json', 'CHANGELOG.md',
                     '.github/workflows/ci.yml')
        for relative in protected:
            (self.destination / relative).write_text('Custom project content\n')
        claude = self.destination / 'CLAUDE.md'
        claude.write_text('Custom project instructions\n\n' + claude.read_text())
        owned = self.destination / '.cursor/rules/core/security.mdc'
        owned.write_text('Outdated rule\n')
        stale = self.destination / '.claude/rules/modules/removed-upstream.md'
        stale.write_text('Stale rule\n')
        custom = self.destination / '.claude/rules/custom.md'
        custom.write_text('Project custom rule\n')
        changelog = self.destination / 'docs/reference/ruleset-changelog.md'
        changelog.write_text('Old ruleset history\n')
        (self.destination / '.ruleset-version').write_text('ruleset=old-fixture\n')
        output = self.install('both', '--update')
        self.assertIn('Ruleset transition: old-fixture ->', output)
        self.assertEqual(changelog.read_bytes(), (ROOT / 'CHANGELOG.md').read_bytes())
        for relative in protected:
            self.assertEqual((self.destination / relative).read_text(),
                             'Custom project content\n', relative)
        self.assertTrue(claude.read_text().startswith('Custom project instructions\n'))
        self.assertEqual(owned.read_bytes(), (ROOT / 'core/security.mdc').read_bytes())
        self.assertFalse(stale.exists())
        self.assertEqual(custom.read_text(), 'Project custom rule\n')
        self.assertIn('@.claude/rules-on-demand/modules/audit-trail.md', claude.read_text())

    def test_invalid_target_fails_without_creating_destination(self) -> None:
        result = subprocess.run(
            ['bash', str(ROOT / 'init.sh'), '--dest', str(self.destination),
             '--target', 'invalid'], capture_output=True, text=True,
            timeout=10, check=False,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('--target must be', result.stderr)
        self.assertFalse(self.destination.exists())
