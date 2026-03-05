#!/usr/bin/env python
"""
Simple DB inspection helper for Inven-Go.
Run from project root inside the virtualenv:
    python scripts/inspect_db.py

It uses the application's SQLAlchemy configuration to connect and prints:
- list of tables
- row counts for a few key tables
- up to 5 sample rows for each key table found
"""
from app import create_app, db
from sqlalchemy import inspect, text
import json

KEY_TABLES = [
    'users',
    'laporan_kerusakan',
    'aset_tetap'
]


def pretty_print_row(row):
    try:
        return json.dumps(dict(row), default=str, indent=2, ensure_ascii=False)
    except Exception:
        # fallback for RowProxy in older SQLAlchemy versions
        return str(row)


def main():
    app = create_app()
    with app.app_context():
        # Use db.engine for compatibility across Flask-SQLAlchemy versions
        engine = db.engine
        inspector = inspect(engine)

        print("\nConnected to database:\n")
        try:
            print(f"  - URL: {app.config.get('SQLALCHEMY_DATABASE_URI')}")
        except Exception:
            pass

        tables = inspector.get_table_names()
        print("\nTables found (count={}):".format(len(tables)))
        for t in tables:
            print(f"  - {t}")

        # Show info for key tables
        for table in KEY_TABLES:
            if table in tables:
                print(f"\n== Table: {table} ==")
                # count
                try:
                    with engine.connect() as conn:
                        count = conn.execute(text(f"SELECT COUNT(*) AS c FROM `{table}`")).fetchone()[0]
                except Exception:
                    # fallback without backticks
                    with engine.connect() as conn:
                        count = conn.execute(text(f"SELECT COUNT(*) AS c FROM {table}")).fetchone()[0]
                print(f"Total rows: {count}")

                # sample rows
                print("Sample rows (up to 5):")
                try:
                    with engine.connect() as conn:
                        rows = conn.execute(text(f"SELECT * FROM `{table}` LIMIT 5")).fetchall()
                except Exception:
                    with engine.connect() as conn:
                        rows = conn.execute(text(f"SELECT * FROM {table} LIMIT 5")).fetchall()

                if not rows:
                    print("  (no rows)")
                else:
                    for r in rows:
                        print(pretty_print_row(r))
                        print("---")
            else:
                print(f"\n== Table: {table} not found ==")

if __name__ == '__main__':
    main()
