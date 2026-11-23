import sys, tempfile, unittest
from datetime import date
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from automate import analyze
class Tests(unittest.TestCase):
 def run_csv(self, content):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'x.csv'; p.write_text(content, encoding='utf-8'); return analyze(p, date(2026,11,24))
 def test_overdue(self):
  r=self.run_csv('task,owner,status,due_date\nA,B,todo,2026-11-01\nC,D,done,2026-11-01\n'); self.assertEqual(len(r['overdue']),1)
 def test_invalid(self): self.assertEqual(len(self.run_csv('task,owner,status,due_date\nA,B,no,xxx\n')['errors']),1)
 def test_missing(self):
  with self.assertRaises(ValueError): self.run_csv('wrong,header\na,b\n')
 def test_duplicate(self):
  with self.assertRaises(ValueError): self.run_csv('task,owner,status,due_date,task\na,b,todo,2026-01-01,c\n')
if __name__ == '__main__': unittest.main()
