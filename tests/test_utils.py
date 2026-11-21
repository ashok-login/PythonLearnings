"""Run from the project root: python -m unittest discover -s tests -v."""

import os
from pathlib import Path
import runpy
import sys
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from utils.uitls import load_env_file


class LoadEnvFileTests(unittest.TestCase):
    def setUp(self):
        self.temp_directory = TemporaryDirectory()
        self.addCleanup(self.temp_directory.cleanup)
        self.root = Path(self.temp_directory.name).resolve()
        # Restore the real environment after each test.
        environment = patch.dict(os.environ, {}, clear=True)
        environment.start()
        self.addCleanup(environment.stop)

    def test_loads_env_from_start_directory(self):
        env_file = self.root / ".env"
        env_file.write_text("UTILS_TEST_VALUE=hello\n", encoding="utf-8")

        result = load_env_file(self.root)

        self.assertEqual(result, env_file)
        self.assertEqual(os.environ["UTILS_TEST_VALUE"], "hello")

    def test_finds_env_in_parent_directory(self):
        env_file = self.root / ".env"
        env_file.write_text("UTILS_TEST_VALUE=parent\n", encoding="utf-8")
        child = self.root / "app" / "services"
        child.mkdir(parents=True)

        result = load_env_file(str(child))

        self.assertEqual(result, env_file)
        self.assertEqual(os.environ["UTILS_TEST_VALUE"], "parent")

    def test_uses_nearest_env_file(self):
        (self.root / ".env").write_text(
            "UTILS_TEST_VALUE=parent\n", encoding="utf-8"
        )
        child = self.root / "app"
        child.mkdir()
        nearest_env = child / ".env"
        nearest_env.write_text("UTILS_TEST_VALUE=child\n", encoding="utf-8")

        result = load_env_file(child)

        self.assertEqual(result, nearest_env)
        self.assertEqual(os.environ["UTILS_TEST_VALUE"], "child")

    def test_preserves_existing_environment_variables(self):
        (self.root / ".env").write_text(
            "UTILS_TEST_VALUE=from_file\n", encoding="utf-8"
        )
        os.environ["UTILS_TEST_VALUE"] = "already_set"

        load_env_file(self.root)

        self.assertEqual(os.environ["UTILS_TEST_VALUE"], "already_set")

    def test_raises_when_no_env_file_exists(self):
        # Isolate this test from any .env files above the temporary directory.
        with patch("utils.uitls.Path.is_file", return_value=False):
            with self.assertRaisesRegex(FileNotFoundError, "Could not find .env"):
                load_env_file(self.root)

    def test_missing_dotenv_dependency_is_reported(self):
        module_path = Path(__file__).resolve().parents[1] / "utils" / "uitls.py"
        with patch.dict(sys.modules, {"dotenv": None}):
            with self.assertRaises(ModuleNotFoundError):
                runpy.run_path(str(module_path))


if __name__ == "__main__":
    unittest.main()
