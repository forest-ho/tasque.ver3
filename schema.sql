CREATE TABLE IF NOT EXISTS users (
    user_id TEXT PRIMARY KEY,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS user_profiles (
    user_id TEXT PRIMARY KEY REFERENCES users(user_id) ON DELETE CASCADE,
    display_name TEXT NOT NULL DEFAULT '冒険者',
    level INTEGER NOT NULL DEFAULT 1 CHECK (level > 0),
    icon TEXT
);

CREATE TABLE IF NOT EXISTS main_tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    due_date TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (user_id, id)
);

CREATE TABLE IF NOT EXISTS monster_batches (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    main_task_id INTEGER NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (user_id, main_task_id, id),
    FOREIGN KEY (user_id, main_task_id)
        REFERENCES main_tasks(user_id, id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS sub_tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    main_task_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    priority TEXT NOT NULL CHECK (priority IN ('高', '中', '低')),
    due_date TEXT NOT NULL,
    completed INTEGER NOT NULL DEFAULT 0 CHECK (completed IN (0, 1)),
    monster_id INTEGER NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id, main_task_id)
        REFERENCES main_tasks(user_id, id) ON DELETE CASCADE,
    FOREIGN KEY (user_id, main_task_id, monster_id)
        REFERENCES monster_batches(user_id, main_task_id, id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS main_tasks_by_user
    ON main_tasks(user_id, created_at DESC);
CREATE INDEX IF NOT EXISTS sub_tasks_by_user_and_main
    ON sub_tasks(user_id, main_task_id, created_at);
CREATE INDEX IF NOT EXISTS monster_batches_by_user_and_main
    ON monster_batches(user_id, main_task_id, created_at);