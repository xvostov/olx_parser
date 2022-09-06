class EmptyPageException(Exception):
    """"Исключение вызывается когда сервер возвращает пустую страницу с кодом 502,
        такое происходит когда запрос выходит за предел пагинации"""
    pass


class MissingPhotoException(Exception):
    pass


class UnsuitableProductError(Exception):
    pass