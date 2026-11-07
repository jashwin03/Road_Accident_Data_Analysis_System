"""CLI entry point."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from config import RAW_DIR, REPORT_DIR
from database.connection import engine, get_session, init_db
from src.analysis import build_trend_report, load_accidents_df
from src.ingest import ingest_csv
from src.seed_data import write_synthetic_csv
from src.visualization import generate_all_charts


def cmd_init_db(_args):
    init_db()
    print("[OK] Database tables created / verified.")


def cmd_seed(args):
    path = RAW_DIR / "accidents_synthetic.csv"
    df = write_synthetic_csv(path, n=args.rows, seed=args.seed)
    print(f"[OK] Wrote {len(df)} synthetic rows -> {path}")
    session = get_session()
    try:
        report = ingest_csv(session, path)
    finally:
        session.close()
    print(f"[OK] Inserted {report['inserted_rows']} rows into the database.")
    print(f"     Dropped rows: {report['dropped_rows']}")
    (REPORT_DIR / "last_ingest_report.json").write_text(
        json.dumps(report, indent=2, default=str), encoding="utf-8"
    )


def cmd_ingest(args):
    path = Path(args.file)
    if not path.exists():
        sys.exit(f"[ERROR] File not found: {path}")
    session = get_session()
    try:
        report = ingest_csv(session, path, dry_run=args.dry_run)
    finally:
        session.close()

    print(f"[OK] File: {path}")
    print(f"     Total rows    : {report['total_rows']}")
    print(f"     Valid rows    : {report['valid_rows']}")
    print(f"     Dropped rows  : {report['dropped_rows']}")
    print(f"     Inserted rows : {report['inserted_rows']}")
    print("     Missing values:")
    for col, cnt in report["missing"].items():
        print(f"       - {col}: {cnt}")
    (REPORT_DIR / "last_ingest_report.json").write_text(
        json.dumps(report, indent=2, default=str), encoding="utf-8"
    )
    print(f"[OK] Validation report -> {REPORT_DIR / 'last_ingest_report.json'}")


def cmd_analyze(_args):
    df = load_accidents_df(engine)
    if df.empty:
        sys.exit("[ERROR] No records. Run `python main.py seed` first.")
    print(f"[OK] Loaded {len(df)} records.")
    report_path = build_trend_report(df)
    print(f"[OK] Trend report   -> {report_path}")
    charts = generate_all_charts(df)
    print(f"[OK] Generated {len(charts)} charts:")
    for c in charts:
        print(f"       - {c}")


def cmd_all(args):
    cmd_init_db(args); cmd_seed(args); cmd_analyze(args)


def build_parser():
    parser = argparse.ArgumentParser(description="Road Accident Data Analysis (Project 13)")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("init-db", help="Create database tables").set_defaults(func=cmd_init_db)

    p_seed = sub.add_parser("seed", help="Generate + load synthetic records")
    p_seed.add_argument("--rows", type=int, default=500)
    p_seed.add_argument("--seed", type=int, default=42)
    p_seed.set_defaults(func=cmd_seed)

    p_ingest = sub.add_parser("ingest", help="Import a CSV file")
    p_ingest.add_argument("--file", required=True)
    p_ingest.add_argument("--dry-run", action="store_true")
    p_ingest.set_defaults(func=cmd_ingest)

    sub.add_parser("analyze", help="Analyse + generate charts").set_defaults(func=cmd_analyze)

    p_all = sub.add_parser("all", help="init-db + seed + analyze")
    p_all.add_argument("--rows", type=int, default=500)
    p_all.add_argument("--seed", type=int, default=42)
    p_all.set_defaults(func=cmd_all)
    return parser


def main():
    args = build_parser().parse_args()
    args.func(args)


if __name__ == "__main__":
    main()