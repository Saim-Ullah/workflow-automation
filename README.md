# Workflow Automation

A dependency-free Python command-line workflow that validates a CSV task list and produces a JSON summary with status counts, overdue tasks and row-level errors. It never changes the input or sends data anywhere. Sample data is fictional.

```sh
python automate.py examples/tasks.csv --as-of 2026-11-24
python automate.py examples/tasks.csv > report.json
python -m unittest discover -s tests -v
```

CSV columns: `task,owner,status,due_date`. Status is `todo`, `doing` or `done`; dates use `YYYY-MM-DD`. Exit codes: 0 all rows valid, 1 some rows invalid (valid rows still reported), 2 file/schema error. Schedule it with Task Scheduler or cron; use `--as-of` for reproducible reports. Reports may contain personal data: review them before sharing.
