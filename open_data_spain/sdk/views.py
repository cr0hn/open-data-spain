from functools import wraps


def get_page(_request, first: int = 1) -> int:
    try:
        page = int(_request.GET.get('page', 1))

        if page < 1:
            page = first

    except ValueError:
        page = first

    return page


def get_page_size(_request, max_allowed: int = 100, default: int = 20) -> int:
    try:
        page_size = int(_request.GET.get('page_size', default))

        if page_size < 1:
            page_size = default

        if page_size > max_allowed:
            page_size = max_allowed
    except ValueError:
        page_size = default

    return page_size


def pagination():
    """
    Decorator to paginate a view. Usage::

        @pagination()
        def my_view(request, page, page_size):
            # I can assume now that only GET or POST requests make it this far
            # ...
    """

    def decorator(func):
        @wraps(func)
        def inner(request, *args, **kwargs):
            page = get_page(request)
            page_size = get_page_size(request, max_allowed=25)

            return func(request, page=page, page_size=page_size, *args, **kwargs)

        return inner

    return decorator


def apagination():
    """
    Decorator to paginate a view. Usage::

        @pagination()
        def my_view(request, page, page_size):
            # I can assume now that only GET or POST requests make it this far
            # ...
    """

    def decorator(func):
        @wraps(func)
        async def inner(request, *args, **kwargs):
            page = get_page(request)
            page_size = get_page_size(request, max_allowed=25)

            return await func(request, page=page, page_size=page_size, *args, **kwargs)

        return inner

    return decorator


__all__ = ('get_page', 'get_page_size', 'pagination', 'apagination')
