import aiosqlite

# Initialize the database and create tables
async def init_db():
    async with aiosqlite.connect('database.db') as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                is_active BOOLEAN DEFAULT TRUE
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS activity (
                user_id INTEGER,
                query_count INTEGER DEFAULT 0,
                FOREIGN KEY(user_id) REFERENCES users(user_id) ON DELETE CASCADE
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS message_logs (
                user_id INTEGER,
                message_type TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS blocked_messages (
                user_id INTEGER,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        await db.commit()

# Add a new user
async def add_user(user_id: int):
    async with aiosqlite.connect('database.db') as db:
        await db.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,))
        await db.commit()

# Increment the user's activity count
async def increment_user_activity(user_id: int):
    async with aiosqlite.connect('database.db') as db:
        await db.execute("UPDATE activity SET query_count = query_count + 1 WHERE user_id = ?", (user_id,))
        await db.commit()


async def log_message(user_id: int, message_type: str):
    async with aiosqlite.connect('database.db') as db:
        await db.execute("INSERT INTO message_logs (user_id, message_type) VALUES (?, ?)", (user_id, message_type))
        await db.commit()

# Log when a bot is blocked)
async def log_blocked_message(user_id: int):
    async with aiosqlite.connect('database.db') as db:
        await db.execute("INSERT INTO blocked_messages (user_id) VALUES (?)", (user_id,))
        await db.commit()
