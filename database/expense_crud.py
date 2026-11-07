import json
from database.db_connection import get_connection

def create_expense(data):
    payload = data.model_dump(mode="json") if hasattr(data, "model_dump") else data
    with get_connection() as conn:
        cur = conn.execute("INSERT INTO expenses (expense_json) VALUES (?)",
                           (json.dumps(payload, ensure_ascii=False),))
        return cur.lastrowid

def get_all_expenses():
    with get_connection() as conn:
        rows = conn.execute("SELECT id, expense_json, created_at, updated_at FROM expenses ORDER BY id DESC").fetchall()
    results = []
    for row in rows:
        try:
            item = json.loads(row["expense_json"])
            item.update({"id": row["id"], "created_at": row["created_at"], "updated_at": row["updated_at"]})
            results.append(item)
        except json.JSONDecodeError:
            continue
    return results

def update_expense(expense_id, data):
    payload = data.model_dump(mode="json") if hasattr(data, "model_dump") else data
    with get_connection() as conn:
        cur = conn.execute(
            "UPDATE expenses SET expense_json=?, updated_at=CURRENT_TIMESTAMP WHERE id=?",
            (json.dumps(payload, ensure_ascii=False), int(expense_id))
        )
        return cur.rowcount > 0

def delete_expense(expense_id):
    with get_connection() as conn:
        cur = conn.execute("DELETE FROM expenses WHERE id=?", (int(expense_id),))
        return cur.rowcount > 0
