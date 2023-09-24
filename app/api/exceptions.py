class InvalidSizeTable(Exception):
    """Исключение возникает при недопустимом размере таблицы."""

    def __init__(self, message, status_code=None):
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code