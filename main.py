"""
===============================================================================
  GroceryPOS Pro - Professional Point of Sale System
  Version: 2.0.0
  Author:  POS Development Team
  License: MIT
===============================================================================
  Entry point for the application. Bootstraps DB, applies theme, and
  launches the main window.
===============================================================================
"""

import os
import sys
import logging
from pathlib import Path

# ── Make sure project root is on sys.path when running from an EXE ──────────
BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

# ── Logging ──────────────────────────────────────────────────────────────────
LOG_FILE = BASE_DIR / "logs" / "app.log"
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger("main")


def main() -> None:
    """Application entry point."""
    logger.info("Starting GroceryPOS Pro v2.0.0")

    # ── Ensure required directories exist ────────────────────────────────────
    for folder in ("logs", "backups", "assets", "reports", "data"):
        (BASE_DIR / folder).mkdir(parents=True, exist_ok=True)

    # ── Database bootstrap ────────────────────────────────────────────────────
    from models.database import DatabaseManager
    db = DatabaseManager()
    db.initialize()
    db.seed_sample_data()
    logger.info("Database ready")

    # ── GUI ───────────────────────────────────────────────────────────────────
    import tkinter as tk
    from views.login_view import LoginView

    root = tk.Tk()
    root.withdraw()          # hide until login succeeds

    app = LoginView(root, db)
    root.deiconify()
    root.mainloop()

    logger.info("Application closed")


if __name__ == "__main__":
    main()
