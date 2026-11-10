from rest_framework.pagination import CursorPagination


class SafeCursorPagination(CursorPagination):
    # CursorPagination не показывает обычные номера страниц и offset.
    # На одной странице максимум 6 объектов.
    page_size = 6

    # Сначала новые записи. ID используется как дополнительная сортировка,
    # чтобы порядок оставался стабильным, если created_at совпадает.
    ordering = ("-created_at", "-pk")
