"""
run_pipeline.py — Master Execution Script
==========================================
Bluestock Fintech | Indian MF Industry Capstone | 2022-2025

Orchestrates all 5 pipeline stages in sequence. Each stage is executed
as a Jupyter notebook via nbconvert, writing intermediate outputs to
the data/ and outputs/ directories.

Usage
-----
    python run_pipeline.py                  # Run all stages
    python run_pipeline.py --stage 3        # Run only stage 3
    python run_pipeline.py --from 2         # Run stages 2-5
    python run_pipeline.py --dry-run        # Print plan, do not execute

Configuration
-------------
    See config.yaml for data paths, AMFI URLs, and feature flags.
"""

import argparse
import logging
import os
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path


# ── Configuration ─────────────────────────────────────────────────────────

STAGES = [
    {
        "id": 1,
        "name": "Data Ingestion",
        "notebook": "notebooks/01_data_ingestion.ipynb",
        "description": "Fetch raw CSVs from AMFI India URLs and store locally.",
        "output_dir": "data/raw",
        "expected_outputs": ["nav_raw.csv", "aum_raw.csv", "sip_raw.csv",
                             "folio_raw.csv", "demographics_raw.csv",
                             "category_inflows_raw.csv", "sector_raw.csv"],
    },
    {
        "id": 2,
        "name": "Data Cleaning",
        "notebook": "notebooks/02_data_cleaning.ipynb",
        "description": "Deduplicate, cast dtypes, handle nulls, standardise scheme names.",
        "output_dir": "data/clean",
        "expected_outputs": ["nav_clean.parquet", "aum_clean.parquet",
                             "sip_clean.parquet", "folio_clean.parquet",
                             "demographics_clean.parquet",
                             "category_inflows_clean.parquet",
                             "sector_clean.parquet"],
    },
    {
        "id": 3,
        "name": "EDA Analysis",
        "notebook": "notebooks/03_eda_analysis.ipynb",
        "description": "Statistical summaries, distributions, correlations, and visualisations.",
        "output_dir": "outputs/charts",
        "expected_outputs": ["sip_inflow_trend.png", "folio_count_growth.png",
                             "age_group_distribution.png", "aum_growth_chart.png",
                             "category_heatmap.png", "sector_allocation_donut.png",
                             "t30_vs_b30_pie.png", "sip_amount_boxplot.png",
                             "nav_trend.png", "correlation_matrix.png",
                             "horizontal_bar_chart.png"],
    },
    {
        "id": 4,
        "name": "Fund Performance Analytics",
        "notebook": "notebooks/04_Fund_Performance_Analytics.ipynb",
        "description": "Rolling returns, Sharpe ratio, max drawdown, alpha, beta, fund ranking.",
        "output_dir": "outputs/analytics",
        "expected_outputs": ["fund_metrics.parquet", "rolling_returns.parquet",
                             "performance_ranking.csv"],
    },
    {
        "id": 5,
        "name": "Advanced Analytics",
        "notebook": "notebooks/05_advanced_analytics.ipynb",
        "description": "Cohort analysis, T30/B30 segmentation, sector heatmaps, ML-ready features.",
        "output_dir": "outputs/advanced",
        "expected_outputs": ["cohort_analysis.parquet", "t30_b30_features.parquet",
                             "ml_features.parquet"],
    },
]

LOG_FORMAT = "%(asctime)s  %(levelname)-8s  %(message)s"
LOG_FILE   = f"pipeline_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"


# ── Helpers ───────────────────────────────────────────────────────────────

def setup_logging(verbose: bool = False) -> logging.Logger:
    """Configure console + file logging."""
    level = logging.DEBUG if verbose else logging.INFO
    handlers = [
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
    ]
    logging.basicConfig(level=level, format=LOG_FORMAT, handlers=handlers)
    return logging.getLogger("pipeline")


def ensure_dirs() -> None:
    """Create all output directories if they do not exist."""
    dirs = [
        "data/raw", "data/clean",
        "outputs/charts", "outputs/analytics", "outputs/advanced",
        "logs",
    ]
    for d in dirs:
        Path(d).mkdir(parents=True, exist_ok=True)


def check_notebook(path: str) -> bool:
    """Return True if the notebook file exists."""
    return Path(path).exists()


def run_notebook(notebook_path: str, timeout: int = 3600) -> tuple[bool, float]:
    """
    Execute a Jupyter notebook via nbconvert.

    Parameters
    ----------
    notebook_path : str
        Relative path to the .ipynb file.
    timeout : int
        Maximum execution time in seconds (default: 1 hour).

    Returns
    -------
    (success: bool, elapsed_seconds: float)
    """
    start = time.time()
    output_path = notebook_path.replace(".ipynb", "_executed.ipynb")

    cmd = [
        "jupyter", "nbconvert",
        "--to", "notebook",
        "--execute",
        "--ExecutePreprocessor.timeout=" + str(timeout),
        "--output", output_path,
        notebook_path,
    ]

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=timeout + 60,
    )
    elapsed = time.time() - start

    return result.returncode == 0, elapsed


def validate_outputs(stage: dict, log: logging.Logger) -> tuple[int, int]:
    """
    Check that expected output files exist after a stage runs.

    Returns
    -------
    (found: int, total: int)
    """
    found = 0
    total = len(stage["expected_outputs"])
    for fname in stage["expected_outputs"]:
        fpath = Path(stage["output_dir"]) / fname
        if fpath.exists():
            found += 1
            log.debug("  ✓ %s", fpath)
        else:
            log.warning("  ✗ Missing expected output: %s", fpath)
    return found, total


def print_banner(log: logging.Logger) -> None:
    """Print pipeline header."""
    log.info("=" * 68)
    log.info("  Bluestock Fintech — Indian MF Industry Capstone Pipeline")
    log.info("  Version: v1.0  |  Run: %s", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    log.info("=" * 68)


def print_summary(results: list[dict], log: logging.Logger) -> None:
    """Print execution summary table."""
    log.info("")
    log.info("─" * 68)
    log.info("PIPELINE SUMMARY")
    log.info("─" * 68)
    log.info("  %-4s  %-28s  %-10s  %-10s  %s",
             "ID", "Stage", "Status", "Duration", "Outputs")
    log.info("  " + "-" * 64)
    for r in results:
        status = "✓ PASS" if r["success"] else "✗ FAIL"
        dur    = f"{r['elapsed']:.1f}s" if r["elapsed"] else "—"
        outs   = f"{r['found']}/{r['total']}" if r["total"] else "—"
        log.info("  %-4s  %-28s  %-10s  %-10s  %s",
                 r["id"], r["name"][:28], status, dur, outs)
    log.info("─" * 68)
    passed = sum(1 for r in results if r["success"])
    log.info("  Result: %d/%d stages passed", passed, len(results))
    log.info("─" * 68)


# ── CLI ───────────────────────────────────────────────────────────────────

def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        prog="run_pipeline.py",
        description="Bluestock Fintech MF Capstone — Master Pipeline Runner",
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--stage", type=int, metavar="N",
        help="Run only stage N (1-5)",
    )
    group.add_argument(
        "--from", dest="from_stage", type=int, metavar="N",
        help="Run stages N through 5",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Print the execution plan without running any notebooks",
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true",
        help="Enable debug logging",
    )
    parser.add_argument(
        "--timeout", type=int, default=3600,
        help="Per-stage timeout in seconds (default: 3600)",
    )
    parser.add_argument(
        "--skip-validation", action="store_true",
        help="Skip output file validation after each stage",
    )
    return parser.parse_args()


# ── Main ──────────────────────────────────────────────────────────────────

def main() -> int:
    """
    Entry point.

    Returns
    -------
    int
        0 on full success, 1 if any stage fails.
    """
    args = parse_args()
    log  = setup_logging(args.verbose)

    ensure_dirs()
    print_banner(log)

    # Select which stages to run
    if args.stage:
        stages_to_run = [s for s in STAGES if s["id"] == args.stage]
        if not stages_to_run:
            log.error("Invalid stage: %d. Must be 1-5.", args.stage)
            return 1
    elif args.from_stage:
        stages_to_run = [s for s in STAGES if s["id"] >= args.from_stage]
    else:
        stages_to_run = STAGES

    log.info("")
    log.info("Stages to execute: %s", [s["id"] for s in stages_to_run])
    log.info("")

    if args.dry_run:
        log.info("DRY RUN — no notebooks will be executed")
        log.info("")
        for s in stages_to_run:
            nb_ok = "✓" if check_notebook(s["notebook"]) else "✗ MISSING"
            log.info("  [%d] %s  (%s)  notebook: %s",
                     s["id"], s["name"], nb_ok, s["notebook"])
        return 0

    results = []
    overall_success = True

    for stage in stages_to_run:
        log.info("")
        log.info("┌─ Stage %d: %s", stage["id"], stage["name"])
        log.info("│  %s", stage["description"])

        # Check notebook exists
        if not check_notebook(stage["notebook"]):
            log.error("│  ✗ Notebook not found: %s", stage["notebook"])
            log.info("└─ Skipping (notebook missing)")
            results.append({
                "id": stage["id"], "name": stage["name"],
                "success": False, "elapsed": None, "found": 0, "total": 0,
            })
            overall_success = False
            continue

        log.info("│  Executing notebook: %s", stage["notebook"])
        log.info("│  Timeout: %ds", args.timeout)

        try:
            success, elapsed = run_notebook(stage["notebook"], timeout=args.timeout)
        except subprocess.TimeoutExpired:
            log.error("│  ✗ Stage timed out after %ds", args.timeout)
            results.append({
                "id": stage["id"], "name": stage["name"],
                "success": False, "elapsed": args.timeout, "found": 0, "total": 0,
            })
            overall_success = False
            continue
        except Exception as exc:
            log.error("│  ✗ Unexpected error: %s", exc)
            results.append({
                "id": stage["id"], "name": stage["name"],
                "success": False, "elapsed": None, "found": 0, "total": 0,
            })
            overall_success = False
            continue

        # Validate outputs
        found = total = 0
        if not args.skip_validation:
            found, total = validate_outputs(stage, log)
            log.info("│  Output validation: %d/%d files found", found, total)

        status = "✓ PASS" if success else "✗ FAIL"
        log.info("└─ %s  (%.1fs)", status, elapsed)

        results.append({
            "id": stage["id"], "name": stage["name"],
            "success": success, "elapsed": elapsed,
            "found": found, "total": total,
        })

        if not success:
            overall_success = False
            log.warning("Stage %d failed — subsequent stages may be affected.", stage["id"])

    print_summary(results, log)
    log.info("Log written to: %s", LOG_FILE)

    return 0 if overall_success else 1


if __name__ == "__main__":
    sys.exit(main())
