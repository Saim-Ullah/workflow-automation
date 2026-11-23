#!/usr/bin/env python3
"""Validate a task CSV and produce an actionable summary without altering input."""
import argparse, csv, json, sys
from collections import Counter
from datetime import date
from pathlib import Path

REQUIRED = {'task', 'owner', 'status', 'due_date'}
STATUSES = {'todo', 'doing', 'done'}
def analyze(path, today):
    tasks, errors = [], []
    with open(path, encoding='utf-8-sig', newline='') as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames or not REQUIRED.issubset(reader.fieldnames):
            raise ValueError('CSV must contain task, owner, status, due_date headers')
        if len(set(reader.fieldnames)) != len(reader.fieldnames): raise ValueError('Duplicate headers')
        for line, row in enumerate(reader, 2):
            try:
                if None in row: raise ValueError('too many columns')
                item = {k: (row.get(k) or '').strip() for k in REQUIRED}
                if not item['task'] or not item['owner']: raise ValueError('task and owner are required')
                item['status'] = item['status'].lower()
                if item['status'] not in STATUSES: raise ValueError('status must be todo, doing, or done')
                due = date.fromisoformat(item['due_date'])
                item['overdue'] = item['status'] != 'done' and due < today
                tasks.append(item)
            except ValueError as e: errors.append({'line': line, 'error': str(e)})
    return {'as_of': today.isoformat(), 'valid_rows': len(tasks), 'status_counts': dict(sorted(Counter(t['status'] for t in tasks).items())), 'overdue': [t for t in tasks if t['overdue']], 'errors': errors}

def main():
    p = argparse.ArgumentParser(description='Validate task CSV and print a JSON report')
    p.add_argument('csv'); p.add_argument('--as-of', type=date.fromisoformat, default=date.today(), help='ISO date, default today')
    a = p.parse_args()
    try: result = analyze(a.csv, a.as_of)
    except (OSError, UnicodeError, ValueError, csv.Error) as e: print(f'Error: {e}', file=sys.stderr); return 2
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 1 if result['errors'] else 0
if __name__ == '__main__': sys.exit(main())
