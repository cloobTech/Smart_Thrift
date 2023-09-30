from models import storage


def get_db():
    try:
        yield storage
    except Exception:
        storage.rollback()
    finally:
        storage.shutdown_db()
