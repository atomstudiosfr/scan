from functools import wraps
from timeit import default_timer

import httpx
from httpx import TimeoutException
from prometheus_client import Counter, Histogram

TOTAL_EXT_HTTP = Counter(
    name="ext_http_requests_total",
    documentation="Total number of external requests by method, status and handler",
    labelnames=("method", "handler", "status",),
)
LATENCY_EXT_HTTP = Histogram(
    name="ext_http_request_duration_seconds",
    documentation="Latency with only few buckets by handler",
    labelnames=("method", "handler",),
    buckets=(0.1, 0.5, 1,)
)


def ext_http_request(function):
    @wraps(function)
    async def wrapper_ext_http_request(*args, **kwargs):
        status = ""
        method = args[1]
        url = args[2]
        handler = url.strip("/")
        if len(handler.split("/", 4)) > 4:
            handler = "/".join(handler.split("/", 4)[:4]) + "/..."
        else:
            handler = "/".join(handler.split("/", 4)[:4])

        start_time = default_timer()
        try:
            result = await function(*args, **kwargs)
            status = result.status_code
        except TimeoutException as error:
            status = "TO"
            raise error
        except Exception as error:
            status = "ERR"
            raise error
        finally:
            duration = default_timer() - start_time
            TOTAL_EXT_HTTP.labels(method=method, handler=handler, status=status).inc()
            LATENCY_EXT_HTTP.labels(method=method, handler=handler).observe(duration)
        return result

    return wrapper_ext_http_request


httpx.AsyncClient.request = ext_http_request(httpx.AsyncClient.request)
