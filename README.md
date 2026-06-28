# GroceryPOS Pro v2.0.0

**Professional Point of Sale System for Grocery & Retail Shops**

---

## Table of Contents
1. [Features](#features)  
2. [Quick Start](#quick-start)  
3. [Default Login Credentials](#default-login-credentials)  
4. [Building the Windows EXE](#building-the-windows-exe)  
5. [Project Structure](#project-structure)  
6. [Database Schema](#database-schema)  
7. [Module Guide](#module-guide)  
8. [Keyboard Shortcuts](#keyboard-shortcuts)  
9. [Roles & Permissions](#roles--permissions)  
10. [Sample Data](#sample-data)  
11. [Running Tests](#running-tests)  
12. [Troubleshooting](#troubleshooting)

---

## Features

| Module | Highlights |
|---|---|
| **Dashboard** | Real-time KPIs, 7-day revenue chart, top sellers, low-stock alerts |
| **Sales / POS** | Barcode scan, cart, discount %, tax, cash/card/wallet, hold & resume, receipt print, returns |
| **Products** | Add/edit/delete, categories, brands, images, expiry, batch, barcode |
| **Inventory** | Stock adjustments (add/remove/damage/count), expiry tracking, damaged-goods log |
| **Customers** | Database, loyalty points, credit balance, purchase history |
| **Suppliers** | Supplier ledger, contact management |
| **Purchase Orders** | Create POs, one-click receive (auto-updates stock) |
| **Accounting** | Revenue vs. COGS, expenses, cash book, daily closing report |
| **Reports** | Sales / Product / Customer / Profit reports → CSV / Excel / PDF |
| **Users** | Admin, Manager, Cashier, Viewer roles; password reset; activity log |
| **Settings** | Store info, tax rate, loyalty rate, invoice prefix, dark/light theme, backup/restore |

---

## Quick Start

### Option A — Run from source (recommended for development)

```bash
# 1. Clone / download the project
# 2. Install Python 3.9+ from https://python.org

# 3. Install dependencies
pip install -r requirements.txt

# 4. Launch the application
python main.py
```

### Option B — Run the Windows EXE

```
1. Download / build GroceryPOS_Pro.exe (see Building section below)
2. Double-click GroceryPOS_Pro.exe
3. Login with admin / admin123
```

---

## Default Login Credentials

| Username | Password | Role |
|---|---|---|
| `admin` | `admin123` | Administrator |
| `cashier1` | `cash123` | Cashier |
| `manager` | `mgr123` | Manager |

> **Change these immediately after first login** via User Management → Edit → Reset Password.

---

## Building the Windows EXE

### Prerequisites
- Windows 10/11
- Python 3.9+ (64-bit recommended)
- pip

### Steps

```bat
REM 1. Open Command Prompt in the project folder
REM 2. Run the build script
build_windows.bat
```

The script will:
1. Install all dependencies including PyInstaller
2. Run the full test suite (fails fast if tests fail)
3. Build `dist\GroceryPOS_Pro\GroceryPOS_Pro.exe`
4. Create required runtime folders

### Manual PyInstaller build

```bash
pip install pyinstaller openpyxl reportlab python-barcode pillow
pyinstaller grocerypos.spec --clean --noconfirm
```

### Distribution
Zip and share the entire `dist\GroceryPOS_Pro\` folder. The app is self-contained — no Python installation required on the end-user machine.

---

## Project Structure

```
pos_system/
├── main.py                   # Entry point
├── requirements.txt
├── grocerypos.spec           # PyInstaller build spec
├── build_windows.bat         # One-click Windows build
│
├── models/
│   ├── __init__.py
│   └── database.py           # DatabaseManager (SQLite, schema, seed, backup)
│
├── views/
│   ├── __init__.py
│   ├── login_view.py         # Login screen
│   ├── main_window.py        # Shell + sidebar navigation
│   ├── dashboard_view.py     # KPI cards + revenue chart
│   ├── sales_view.py         # POS billing interface
│   ├── products_view.py      # Product CRUD
│   ├── inventory_view.py     # Stock management
│   ├── customers_view.py     # Customer management
│   ├── suppliers_view.py     # Supplier management
│   ├── purchases_view.py     # Purchase orders
│   ├── accounting_view.py    # Income/expenses/cash book
│   ├── reports_view.py       # All reports
│   ├── users_view.py         # User management
│   └── settings_view.py      # System settings
│
├── utils/
│   ├── __init__.py
│   ├── theme.py              # Light/dark colour palettes + ttk styles
│   ├── widgets.py            # Reusable UI components
│   └── helpers.py            # Invoice gen, export, receipt, barcode, etc.
│
├── tests/
│   └── test_pos_system.py    # 69 automated tests
│
├── data/                     # SQLite DB (auto-created)
├── backups/                  # Database backups
├── logs/                     # Application logs
├── reports/                  # Exported CSV/Excel/PDF files
└── assets/                   # Images, icons
```

---

## Database Schema

```
users              – Login, roles, permissions
activity_logs      – Every user action timestamped
categories         – Product categories
brands             – Product brands
suppliers          – Supplier directory
products           – Product master (barcode, prices, stock, expiry, batch)
customers          – Customer database (loyalty points, credit)
sales              – Sale header (invoice, totals, payment method)
sale_items         – Individual line items per sale
returns            – Return/refund header
return_items       – Items returned per return
purchase_orders    – PO header
purchase_order_items – PO line items
expenses           – Business expenses (rent, electricity, etc.)
stock_adjustments  – All stock changes with reason & user
held_orders        – Parked/held cart sessions
settings           – Key-value store for all app settings
```

---

## Module Guide

### Sales / POS (F2)
- **Scan/Search**: Type barcode or product name → press Enter or click Search
- **Add to cart**: Press Enter on barcode field, or double-click in search popup
- **Discount**: Enter % in the Discount field (applies to entire order)
- **Hold order (F8)**: Park the current cart with a label
- **Resume order**: Click "▶ Resume" from the Held Orders list
- **Payment (F10)**: Opens payment dialog with quick-amount buttons
- **New sale (F9)**: Clear cart and start fresh
- **Returns**: Click "↩ Return / Refund", search by invoice number

### Products (F3)
- **Add product**: Fill form → Save (barcode must be unique if provided)
- **Expiry tracking**: Set Expiry Date → view in Inventory → Expiry tab
- **Batch numbers**: For tracking product batches
- **Low stock alert**: Set per-product threshold; shown on Dashboard

### Inventory (F4)
- **Stock adjustment types**:
  - *Add Stock*: Received new stock (positive delta)
  - *Remove Stock*: Manually remove (shrinkage, correction)
  - *Damaged / Write-off*: Records in Damaged Goods log
  - *Count Adjustment*: Set absolute quantity from physical count
- **Expiry filter**: Set "Days ahead" to find products expiring soon

### Reports
- All reports support **date range presets** (Today / Week / Month / Year)
- Export to **CSV**, **Excel (.xlsx)**, or **PDF** with one click
- Excel export requires `openpyxl` (installed via requirements.txt)
- PDF export requires `reportlab` (installed via requirements.txt)

### Accounting
- **Daily Closing**: Generates a formatted P&L summary for the day
- **Cash Book**: Auto-populated from cash sales + expenses
- **Overview**: Date-range P&L with daily breakdown table

### Settings
- **Backup**: One-click backup to `backups/` folder with timestamp
- **Restore**: Browse and restore any previous backup (requires restart)
- **Theme**: Light / Dark (apply via ⚙ Settings → System or 🌙 toggle in header)

---

## Keyboard Shortcuts

| Key | Action |
|---|---|
| `F1` | Go to Dashboard |
| `F2` | Go to Sales / POS + focus barcode field |
| `F3` | Go to Products |
| `F4` | Go to Inventory |
| `F5` | Go to Customers |
| `F8` | Hold current order |
| `F9` | New sale (clear cart) |
| `F10` | Open payment dialog |
| `F12` | Go to Settings |
| `Enter` | Scan/search barcode (in POS barcode field) |
| `Enter` | Confirm (in dialogs) |

---

## Roles & Permissions

| Feature | Admin | Manager | Cashier | Viewer |
|---|:---:|:---:|:---:|:---:|
| Sales / POS | ✅ | ✅ | ✅ | ❌ |
| Products CRUD | ✅ | ✅ | ❌ | ❌ |
| Inventory Adjust | ✅ | ✅ | ❌ | ❌ |
| Customer CRUD | ✅ | ✅ | ✅ | ❌ |
| Suppliers | ✅ | ✅ | ❌ | ❌ |
| Purchase Orders | ✅ | ✅ | ❌ | ❌ |
| Accounting | ✅ | ✅ | ❌ | ❌ |
| Reports | ✅ | ✅ | ❌ | ✅ |
| User Management | ✅ | ❌ | ❌ | ❌ |
| Settings | ✅ | ❌ | ❌ | ❌ |

> Role enforcement is at the view level. In production, add server-side validation if needed.

---

## Sample Data

The database is seeded automatically on first run with:

- **3 users**: admin, cashier1, manager
- **13 settings**: store name, currency, tax, loyalty rate, invoice prefix, etc.
- **10 categories**: Beverages, Dairy, Bakery, Snacks, etc.
- **10 brands**: Nestle, Unilever, PepsiCo, etc.
- **4 suppliers**: Al-Fatah, Metro, Nestle Pakistan, National Foods
- **20 products**: Common grocery items with barcodes, prices, expiry dates
- **4 customers**: Walk-in + 3 named customers with loyalty points
- **7 days of sales**: Random transactions for dashboard charts
- **3 expenses**: Electricity, Rent, Salaries

---

## Running Tests

```bash
# Run all 69 tests
python tests/test_pos_system.py

# Run specific test class
python -m unittest tests.test_pos_system.TestHelpers -v
python -m unittest tests.test_pos_system.TestDatabase -v
python -m unittest tests.test_pos_system.TestBusinessLogic -v
```

### Test Coverage

| Class | Tests | Coverage |
|---|---|---|
| `TestHelpers` | 21 | Password hashing, invoice gen, currency format, dates, barcode, receipt |
| `TestDatabase` | 30 | Schema, seed data, CRUD for all tables, constraints, backup |
| `TestBusinessLogic` | 18 | Full sale workflow, payments, discount/tax/change, loyalty, returns, reports |
| **Total** | **69** | |

---

## Troubleshooting

### App won't start
- Check `logs/app.log` for errors
- Ensure Python 3.9+ is installed: `python --version`
- Delete `data/pos_database.db` to reset (loses all data)

### Dark mode looks broken
- Switch back to light: Settings → System → Theme → Light → Save

### Barcode not scanning
- Make sure the barcode field (top of POS) is focused (click it or press F2)
- USB barcode scanners send Enter automatically — this works natively

### Export not opening
- Excel export requires `openpyxl`: `pip install openpyxl`
- PDF export requires `reportlab`: `pip install reportlab`
- Files are saved in the `reports/` folder regardless

### EXE build fails
- Try: `pip install --upgrade pyinstaller`
- On Windows, run as Administrator if permission errors occur
- Check antivirus isn't blocking PyInstaller

### Database locked error
- Close all other instances of the app
- Check `logs/app.log` for details

---

## Architecture Notes

- **MVC Pattern**: Models (`models/`), Views (`views/`), Controllers embedded in views
- **Thread Safety**: All DB access uses a context manager with WAL mode and row factory
- **Error Handling**: Every DB operation wrapped in try/except; errors logged + shown as toasts
- **Input Validation**: All form fields validated before DB write (types, required fields, ranges)
- **Offline First**: 100% local SQLite — no internet required
- **Extensible**: Add new views by creating a class with `__init__(self, master, db, user)` and registering it in `main_window.py`

---

*GroceryPOS Pro v2.0.0 — Built with Python, Tkinter, SQLite*
