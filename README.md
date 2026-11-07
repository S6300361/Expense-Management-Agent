# Expense Management Agent

A Python + Streamlit expense tracker with optional OpenAI natural-language extraction, JSON records stored in SQLite, dynamically generated dashboard filters, and CRUD operations.

## Requirements
- Python 3.10+
- An OpenAI API key for AI entry (manual entry works without it)

## Windows PowerShell setup

```powershell
cd path\to\Expense_Management_Agent
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Add your OpenAI API key to `.env` for AI entry. The manual-entry and database features do not require an API key.

## Run

```powershell
python -m streamlit run app.py
```

## Features
- Natural-language expense extraction into validated JSON (OpenAI API)
- Manual expense entry
- JSON stored in SQLite
- Dashboard filters discovered from available JSON fields
- Analytics and CSV export
- Create, read, update, delete operations
- `.env`, `.env.example`, and `.gitignore` included

## Data and security notes
- The local `.env` file and SQLite database are ignored by Git.
- Review AI-extracted data before saving.
- Do not commit API keys or real personal financial records.
- Back up the local database separately if you need to preserve records.
- Dynamic filters support categorical fields and numeric ranges. Add custom JSON fields through the JSON editor; they will appear in the dashboard when records contain them.

## Git initialization

```powershell
git init
git status
git add .
git commit -m "Initial expense management agent"
```

Check that `.env` and `database/expenses.db` are not staged.
