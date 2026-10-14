import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DB_PATH = ROOT / "data" / "tasque.sqlite3"


def initialize_database(db_path: Path = DB_PATH) -> None:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(db_path) as connection:
        connection.execute("PRAGMA foreign_keys = ON")
        schema = (ROOT / "schema.sql").read_text(encoding="utf-8")
        connection.executescript(schema)
        sub_task_columns = {
            row[1] for row in connection.execute("PRAGMA table_info(sub_tasks)")
        }
        if "completed" not in sub_task_columns:
            connection.execute(
                "ALTER TABLE sub_tasks ADD COLUMN completed INTEGER NOT NULL DEFAULT 0"
            )


def ensure_user(user_id: str, db_path: Path = DB_PATH) -> None:
    initialize_database(db_path)
    with sqlite3.connect(db_path) as connection:
        connection.execute("PRAGMA foreign_keys = ON")
        connection.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,))
        connection.execute(
            "INSERT OR IGNORE INTO user_profiles (user_id) VALUES (?)", (user_id,)
        )


def get_user_profile(user_id: str, db_path: Path = DB_PATH) -> dict:
    ensure_user(user_id, db_path)
    with sqlite3.connect(db_path) as connection:
        row = connection.execute(
            "SELECT display_name, level, icon FROM user_profiles WHERE user_id = ?",
            (user_id,),
        ).fetchone()
    if row is None:
        raise RuntimeError(f"Profile was not created for user {user_id}")
    return {"display_name": row[0], "level": row[1], "icon": row[2]}


def create_main_task(
    user_id: str,
    name: str,
    due_date: str,
    db_path: Path = DB_PATH,
) -> int:
    ensure_user(user_id, db_path)
    normalized_name = name.strip()
    if not normalized_name:
        raise ValueError("Main task name cannot be empty")
    with sqlite3.connect(db_path) as connection:
        connection.execute("PRAGMA foreign_keys = ON")
        cursor = connection.execute(
            "INSERT INTO main_tasks (user_id, name, due_date) VALUES (?, ?, ?)",
            (user_id, normalized_name, due_date),
        )
        return int(cursor.lastrowid)


def list_main_tasks(user_id: str, db_path: Path = DB_PATH) -> list[dict]:
    ensure_user(user_id, db_path)
    with sqlite3.connect(db_path) as connection:
        rows = connection.execute(
            """
            SELECT id, name, due_date
            FROM main_tasks
            WHERE user_id = ?
            ORDER BY created_at DESC, id DESC
            """,
            (user_id,),
        ).fetchall()
    return [{"id": row[0], "name": row[1], "due_date": row[2]} for row in rows]


def create_sub_task(
    user_id: str,
    main_task_id: int,
    name: str,
    priority: str,
    due_date: str,
    db_path: Path = DB_PATH,
) -> int:
    return create_sub_tasks(
        user_id,
        main_task_id,
        [{"name": name, "priority": priority, "due_date": due_date}],
        db_path,
    )[0]


def create_sub_tasks(
    user_id: str,
    main_task_id: int,
    tasks: list[dict],
    db_path: Path = DB_PATH,
) -> list[int]:
    ensure_user(user_id, db_path)
    normalized_tasks = []
    for task in tasks:
        normalized_name = task["name"].strip()
        priority = task["priority"]
        if not normalized_name:
            raise ValueError("Subtask name cannot be empty")
        if priority not in {"高", "中", "低"}:
            raise ValueError("Priority must be 高, 中, or 低")
        normalized_tasks.append(
            (user_id, main_task_id, normalized_name, priority, task["due_date"])
        )
    with sqlite3.connect(db_path) as connection:
        connection.execute("PRAGMA foreign_keys = ON")
        owns_task = connection.execute(
            "SELECT 1 FROM main_tasks WHERE user_id = ? AND id = ?",
            (user_id, main_task_id),
        ).fetchone()
        if owns_task is None:
            raise ValueError("Main task does not belong to this user")
        cursors = [
            connection.execute(
                """
                INSERT INTO sub_tasks (user_id, main_task_id, name, priority, due_date)
                VALUES (?, ?, ?, ?, ?)
                """,
                task,
            )
            for task in normalized_tasks
        ]
        return [int(cursor.lastrowid) for cursor in cursors]


def list_sub_tasks(
    user_id: str,
    main_task_id: int,
    db_path: Path = DB_PATH,
) -> list[dict]:
    ensure_user(user_id, db_path)
    with sqlite3.connect(db_path) as connection:
        rows = connection.execute(
            """
            SELECT id, name, priority, due_date, completed
            FROM sub_tasks
            WHERE user_id = ? AND main_task_id = ?
            ORDER BY created_at, id
            """,
            (user_id, main_task_id),
        ).fetchall()
    return [
        {
            "id": row[0],
            "name": row[1],
            "priority": row[2],
            "due_date": row[3],
            "completed": bool(row[4]),
        }
        for row in rows
    ]


def complete_sub_task(
    user_id: str,
    main_task_id: int,
    sub_task_id: int,
    db_path: Path = DB_PATH,
) -> bool:
    ensure_user(user_id, db_path)
    with sqlite3.connect(db_path) as connection:
        cursor = connection.execute(
            """
            UPDATE sub_tasks
            SET completed = 1
            WHERE user_id = ? AND main_task_id = ? AND id = ? AND completed = 0
            """,
            (user_id, main_task_id, sub_task_id),
        )
        return cursor.rowcount == 1
