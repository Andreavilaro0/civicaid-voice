"""Tests for Q1.1 validation scripts."""
import subprocess
import sys
import os
import json
import tempfile

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def _run(script, *args):
    return subprocess.run(
        [sys.executable, os.path.join(REPO, "scripts", script), *args],
        capture_output=True, text=True, cwd=REPO,
    )


class TestValidateSourceRegistry:
    def test_validates(self):
        r = _run("validate_source_registry.py")
        assert r.returncode == 0, f"FAIL:\n{r.stdout}\n{r.stderr}"
        assert "PASS" in r.stdout


class TestValidatePolicy:
    def test_validates(self):
        r = _run("validate_policy.py")
        assert r.returncode == 0, f"FAIL:\n{r.stdout}\n{r.stderr}"
        assert "PASS" in r.stdout


class TestValidateProcedureDoc:
    def test_sample_validates(self):
        sample = os.path.join(
            REPO, "docs", "arreglos chat", "fase-3", "q1-sources",
            "evidence", "samples", "proceduredoc.sample.json",
        )
        r = _run("validate_proceduredoc_schema.py", sample)
        assert r.returncode == 0, f"FAIL:\n{r.stdout}\n{r.stderr}"
        assert "PASS" in r.stdout

    def test_invalid_proceduredoc_rejected(self):
        """A ProcedureDoc missing required fields should fail validation."""
        invalid = {"version": 1, "id": "test", "nombre": "Test"}
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        ) as f:
            json.dump(invalid, f)
            f.flush()
            r = _run("validate_proceduredoc_schema.py", f.name)
        os.unlink(f.name)
        assert r.returncode != 0, f"Expected FAIL for invalid doc:\n{r.stdout}"
        assert "FAIL" in r.stdout

    def test_missing_file_rejected(self):
        """Passing a nonexistent file should fail."""
        r = _run("validate_proceduredoc_schema.py", "/tmp/nonexistent_doc.json")
        assert r.returncode != 0
