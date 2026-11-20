"""Inspect Schedule Inbox events directly in PostgreSQL."""
import json

import app


def main():
    if not app.USE_POSTGRES:
        raise SystemExit("PostgreSQL is not configured. Check the app's .env file.")

    import psycopg

    try:
        with app.database() as db:
            db.execute("SET TRANSACTION READ ONLY")
            name = db.execute("SELECT current_database() AS name").fetchone()["name"]
            events = db.execute(
                "SELECT id, title, starts_at, ends_at, zone, all_day, summary "
                "FROM events ORDER BY starts_at, id"
            ).fetchall()
    except psycopg.Error as error:
        detail = error.diag.message_primary or type(error).__name__
        raise SystemExit(f"Database check failed: {detail}") from None

    print(f"Connected to {name}. {len(events)} saved event(s).")
    print(json.dumps(events, indent=2))


if __name__ == "__main__":
    main()
