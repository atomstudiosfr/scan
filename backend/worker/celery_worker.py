import ssl

from celery import Celery, signals
from prometheus_client import start_http_server

from core.config import SETTINGS

tasks_lists = [
    'worker.tasks.database',
]

app = Celery(
    'worker',
    broker=f'{SETTINGS.REDIS_DSN}',
    include=tasks_lists,
)

# Optional configuration, see the application user guide.
app.conf.update(
    # consumer_prefetch_multiplier=32,  # default value 4
    task_create_missing_queues=True,
    broker_use_ssl={'ssl_cert_reqs': ssl.CERT_REQUIRED},  # To disable for using in local
    #    consumer_send_task_events=True,
    #    task_send_sent_event=True,
    #    task_track_started=True,
    enable_utc=True,
    timezone='Europe/Paris',
    consumer_hijack_root_logger=False,
    task_reject_on_consumer_lost=True,
    # consumer_disable_rate_limits=True,
    consumer_max_tasks_per_child=10000,
    # optimization="fair",
    # result_expires=1,
    # consumer_revokes_max=100,
    # consumer_revoke_expires=1800,
    # consumer_successful_expires=1800,
    task_default_priority=5,
    task_queue_max_priority=10,
    worker_max_tasks_per_child=50000,
)
app.conf.broker_transport_options = {
    'queue_order_strategy': 'priority',
}

app.amqp.argsrepr_maxsize = 10000


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    pass
    # sender.add_periodic_task(300, task_retry_address_saved_but_not_in_address_correction_request.s())  # 5 min


@signals.worker_ready.connect
def at_start(sender, **k):
    with sender.app.connection() as conn:
        sender.app.send_task('worker.tasks.database.task_init_database', connection=conn)


@signals.celeryd_init.connect
def signals_init(sender, **k):
    start_http_server(80)


if __name__ == '__main__':
    app.start()
