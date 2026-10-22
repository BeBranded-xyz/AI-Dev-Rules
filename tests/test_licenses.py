"""Exercise templates/scripts/check-licenses.mjs with pnpm-shaped input."""

from pathlib import Path
import json
import shutil
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'templates/scripts/check-licenses.mjs'


@unittest.skipUnless(shutil.which('node'), 'node is required for the license script')
class LicenseCheckTests(unittest.TestCase):
    def run_check(self, licenses: dict[str, list[str]]) -> subprocess.CompletedProcess[str]:
        payload = {
            license: [{'name': name, 'versions': ['1.0.0']} for name in names]
            for license, names in licenses.items()
        }
        return subprocess.run(
            ['node', str(SCRIPT)], input=json.dumps(payload), capture_output=True,
            text=True, timeout=30, check=False,
        )

    def assert_allowed(self, expression: str) -> None:
        result = self.run_check({expression: ['fixture-package']})
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def assert_rejected(self, expression: str) -> None:
        result = self.run_check({expression: ['fixture-package']})
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn('fixture-package', result.stderr)

    def test_allows_single_allowlisted_licenses(self) -> None:
        for expression in ('MIT', 'Apache-2.0', 'BSD-3-Clause', 'ISC', 'MPL-2.0'):
            with self.subTest(expression=expression):
                self.assert_allowed(expression)

    def test_rejects_single_disallowed_licenses(self) -> None:
        for expression in ('GPL-3.0', 'AGPL-3.0-only', 'SSPL-1.0', 'BUSL-1.1', 'UNLICENSED'):
            with self.subTest(expression=expression):
                self.assert_rejected(expression)

    def test_or_requires_one_allowed_option(self) -> None:
        self.assert_allowed('(MIT OR GPL-3.0-or-later)')
        self.assert_allowed('GPL-3.0 OR Apache-2.0')
        self.assert_rejected('GPL-3.0 OR PROPRIETARY')

    def test_and_requires_every_license_allowed(self) -> None:
        self.assert_allowed('(MIT AND Apache-2.0)')
        self.assert_rejected('MIT AND GPL-3.0')
        self.assert_rejected('(Apache-2.0 AND AGPL-3.0-only)')

    def test_and_binds_tighter_than_or(self) -> None:
        self.assert_allowed('MIT OR GPL-3.0 AND AGPL-3.0-only')
        self.assert_rejected('GPL-3.0 OR AGPL-3.0-only AND MIT')
        self.assert_allowed('(GPL-3.0 OR MIT) AND Apache-2.0')

    def test_operators_are_case_insensitive(self) -> None:
        self.assert_allowed('MIT or GPL-3.0')
        self.assert_rejected('MIT and GPL-3.0')

    def test_with_exceptions_are_not_allowlisted(self) -> None:
        self.assert_rejected('GPL-2.0-only WITH Classpath-exception-2.0')

    def test_malformed_expressions_fail_closed(self) -> None:
        for expression in ('(MIT OR Apache-2.0', 'MIT OR', 'AND MIT', 'MIT Apache-2.0', ''):
            with self.subTest(expression=expression):
                self.assert_rejected(expression)

    def test_reports_every_violation(self) -> None:
        result = self.run_check({'GPL-3.0': ['first-package'], 'MIT': ['fine-package'],
                                 'MIT AND AGPL-3.0-only': ['second-package']})
        self.assertEqual(result.returncode, 1)
        self.assertIn('first-package', result.stderr)
        self.assertIn('second-package', result.stderr)
        self.assertNotIn('fine-package', result.stderr)

    def test_empty_input_fails(self) -> None:
        result = subprocess.run(['node', str(SCRIPT)], input='', capture_output=True,
                                text=True, timeout=30, check=False)
        self.assertEqual(result.returncode, 1)
        self.assertIn('no input', result.stderr)
