"""Testes do sd.py: python3 -I scripts/test_sd.py"""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SD = Path(__file__).resolve().parent / "sd.py"

JS = """// cabeçalho
// mais um comentário
// e outro

const usersRepo = {
  async insert(user) {
    return db.query('insert into users values ($1)', [user]);
  },
};

function createUser(req, res) {
  return usersRepo.insert(req.body);
}
"""


def run(cwd, *args):
    return subprocess.run([sys.executable, "-I", str(SD), *args], cwd=cwd, capture_output=True, text=True)


class SdTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / "src").mkdir()
        (self.root / "src" / "users.js").write_text(JS, encoding="utf-8")
        (self.root / "package.json").write_text(json.dumps({"dependencies": {"pg": "^8.0.0", "express": "^4"}}))
        (self.root / "package-lock.json").write_text(json.dumps({"packages": {"": {}, "node_modules/pg": {"version": "8.0.0"}}}))
        r = run(self.root, "init")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.map = self.root / ".system-design" / "map.json"
        self.map.write_text(json.dumps({
            "project": {"name": "t"},
            "nodes": [{"id": "api", "label": "API", "type": "service", "tech": "express"}],
            "flows": [{"id": "create-user", "label": "Criar usuário", "steps": [
                # código desceu 3 linhas: insert está na 6, createUser na 11
                {"id": "repo", "label": "Repo", "summary": "s", "file": "src/users.js", "lines": "3-5", "symbol": "usersRepo.insert"},
                {"id": "ctl", "label": "Ctl", "summary": "s", "file": "src/users.js", "lines": "8-10", "symbol": "createUser"},
            ]}],
        }))

    def tearDown(self):
        self.tmp.cleanup()

    def test_check_and_fix(self):
        r = run(self.root, "check")
        self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
        self.assertIn("passo repo: src/users.js linhas 3-5 → 6-8", r.stdout)
        self.assertIn("passo ctl: src/users.js linhas 8-10 → 11-13", r.stdout)
        self.assertIn("possível componente fora do mapa: pg (package.json)", r.stdout)
        self.assertIn("sem varredura de CVEs", r.stdout)
        self.assertNotIn("express (", r.stdout)
        r = run(self.root, "check", "--fix")
        self.assertIn("corrigido: fluxo create-user, passo repo", r.stdout)
        steps = json.loads(self.map.read_text())["flows"][0]["steps"]
        self.assertEqual([s["lines"] for s in steps], ["6-8", "11-13"])
        self.assertTrue((self.root / ".system-design" / "index.html").exists())
        r = run(self.root, "check")
        self.assertNotIn("linhas", r.stdout)

    def test_init_twice_keeps_map(self):
        before = self.map.read_text()
        r = run(self.root, "init")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(self.map.read_text(), before)
        skill = json.loads((self.root / ".system-design" / "skill.json").read_text())
        self.assertEqual(skill["source"], str(SD))

    def test_version(self):
        self.assertTrue(run(self.root, "version").stdout.startswith("system-design "))


if __name__ == "__main__":
    unittest.main()
