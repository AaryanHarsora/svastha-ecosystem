from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from config import DATABASE_URL

# ── Engine ────────────────────────────────────────────────────
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,      # drops stale connections automatically
    pool_size=5,
    max_overflow=10,
    echo=False,              # set True to log all SQL in terminal
)

# ── Session factory ───────────────────────────────────────────
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)

# ── Base class for all ORM models ─────────────────────────────
class Base(DeclarativeBase):
    pass

# ── Dependency — used in every API route ─────────────────────
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ── Quick connection test ─────────────────────────────────────
def test_connection():
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("MariaDB connected successfully")
            return True
    except Exception as e:
        print(f"Connection failed: {e}")
        return False