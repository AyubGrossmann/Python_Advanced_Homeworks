import logging
import time


http_logger = logging.getLogger("project.http")


class HttpRequestLoggingMiddleware:
    # Записываем метод, путь, статус ответа и время обработки запроса.
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.monotonic()

        try:
            response = self.get_response(request)
        except Exception:
            duration = time.monotonic() - start_time
            http_logger.exception(
                "%s %s завершился ошибкой за %.3f сек.",
                request.method,
                request.path,
                duration,
            )
            raise

        duration = time.monotonic() - start_time
        http_logger.info(
            "%s %s -> %s (%.3f сек.)",
            request.method,
            request.path,
            response.status_code,
            duration,
        )
        return response
