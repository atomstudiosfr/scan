from celery import shared_task

from core.utils import sync


@shared_task(queue='scrapper', priority=10)
@sync
async def task_scrap():
    pass


if __name__ == '__main__':
    task_scrap()
