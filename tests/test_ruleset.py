"""Static checks for the distributed rules and their documented activation."""

from pathlib import Path
import re
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[1]
RULES = sorted(
    path for folder in ('core', 'languages', 'platforms', 'modules')
    for path in (ROOT / folder).glob('*.mdc')
)


class RulesetTests(unittest.TestCase):
    def test_frontmatter_and_checklists(self) -> None:
        for path in RULES:
            with self.subTest(rule=str(path.relative_to(ROOT))):
                content = path.read_text(encoding='utf-8')
                self.assertTrue(content.startswith('---\n'))
                _, metadata, body = content.split('---\n', 2)
                self.assertRegex(metadata, r'(?m)^description: .+')
                self.assertRegex(metadata, r'(?m)^alwaysApply: (true|false)$')
                self.assertRegex(body, r'(?m)^## Checklist')
                if path.parent.name in ('languages', 'modules'):
                    self.assertRegex(body, r'(?m)^## Testing')

    def test_activation_catalogue_matches_rules(self) -> None:
        identity = (ROOT / 'PROJECT.md').read_text(encoding='utf-8')
        actual = set(re.findall(r'^- \[ \] `([^`]+)`', identity, re.M))
        expected = {p.stem for p in RULES if p.parent.name != 'core'}
        expected.add('maintenance')
        self.assertEqual(actual, expected)

    def test_explicit_rule_references_resolve(self) -> None:
        sources = RULES + [ROOT / 'README.md', ROOT / 'PROJECT.md', ROOT / 'CHANGELOG.md']
        sources += list((ROOT / 'claude/skills').glob('*/SKILL.md'))
        sources += list((ROOT / 'templates').glob('*.md'))
        names = {p.name for p in RULES}
        pattern = r'`((?:(?:core|modules|languages|platforms)/)?[\w-]+\.mdc)`'
        for path in sources:
            for reference in re.findall(pattern, path.read_text(encoding='utf-8')):
                with self.subTest(source=str(path), reference=reference):
                    if '/' in reference:
                        self.assertTrue((ROOT / reference).is_file())
                    else:
                        self.assertIn(reference, names)

    def test_shell_syntax(self) -> None:
        scripts = [ROOT / 'init.sh', *ROOT.glob('claude/hooks/*.sh')]
        scripts += list(ROOT.glob('templates/scripts/*.sh'))
        for path in scripts:
            with self.subTest(script=str(path)):
                result = subprocess.run(
                    ['bash', '-n', str(path)], capture_output=True, text=True,
                    timeout=10, check=False,
                )
                self.assertEqual(result.returncode, 0, result.stderr)
