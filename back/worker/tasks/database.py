from alembic import command
from celery import shared_task

from core import db as database
from core.config import ALEMBIC_CONFIG
from core.utils import sync


@shared_task(queue='db', priority=10)
@sync
async def task_init_database():
    db = await database.get_db_worker()
    try:
        command.upgrade(ALEMBIC_CONFIG, 'head')
    except Exception as e:
        raise e
    finally:
        await db.aclose()


if __name__ == '__main__':
    task_init_database()
