# SE_LAB5 – Static Code Analysis Lab

## 🧾 Overview
This lab demonstrates how to identify and fix issues in Python code using **static analysis tools** such as **Pylint**, **Bandit**, and **Flake8**.  
The task involved analyzing a given `inventory_system.py` file, detecting potential bugs, security risks, and style issues, and producing a cleaned, well-structured version (`cleaned_inventory_system.py`).  

---

## 📂 Files in Repository

| File Name | Description |
|------------|-------------|
| `inventory_system.py` | Original buggy/insecure code provided in the lab |
| `cleaned_inventory_system.py` | Corrected and optimized version after static analysis |
| `pylint_report.txt` | Pylint output — code quality and convention violations |
| `bandit_report.txt` | Bandit output — security issue scan |
| `flake8_report.txt` | Flake8 output — style and PEP8 compliance report |
| `readme.md` | Overview of the project and reflection answers |

---

## ⚙️ Tools Used
- **Python 3.10+**
- **Pylint** – code quality and convention checking  
- **Bandit** – security analysis  
- **Flake8** – style and PEP8 compliance  
- **Git / GitHub** – version control and submission  
- **macOS Terminal / Codespace** – development environment  

---

## 🧩 Known Issues & Fixes (Before and After Cleaning)

| Issue Type | Line(s) | Description | Fix Applied |
|-------------|----------|-------------|--------------|
| Mutable default argument | 11 | Used `logs=[]` which shares state across calls | Replaced with `logs=None` and initialized inside function |
| Bare `except:` | 25 | Hides actual exceptions | Replaced with `except Exception as e:` and proper logging |
| Unsafe `eval()` | 60 | Dangerous code execution vulnerability | Removed entirely |
| Missing input validation | 12–35 | No checks for data types of `item` and `qty` | Added type checks with `ValueError` and `KeyError` |
| Unhandled File I/O | 40–60 | Used open() without context managers | Replaced with `with open(...)` for safe handling |
| Missing logging | Whole file | No structured logging or debugging info | Added `logging` module with formatted handlers |
| Global variable misuse | All | Unclear global data modifications | Added `_stock_data` with clear scope and type hints |

---

## 🧮 Steps Performed

1. **Analyzed** original `inventory_system.py` using:
   ```bash
   pylint inventory_system.py
   bandit -r inventory_system.py
   flake8 inventory_system.py

