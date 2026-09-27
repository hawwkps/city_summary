

class ExternalServiceError(Exception):
    """Поднимается, когда внешний сервис недоступен после всех попыток"""
    pass


class NotFoundError(Exception):
    """Город или валюта не найдены"""
    pass


