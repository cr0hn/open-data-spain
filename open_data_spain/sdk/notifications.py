import requests


class NotificationException(Exception):
    pass


def notify_pushover(title: str, message: str):
    """Send a notification to Pushover."""

    PUSHOVER_TOKEN = "a9qwptsz2zrtu6mkzgz1fnbp4gzqtv"
    PUSHOVER_USER = "umcz6c3a2tomh7ndxdoq8ici2nk6ar"

    try:
        requests.post(
            "https://api.pushover.net/1/messages.json",
            data={
                "token": PUSHOVER_TOKEN,
                "user": PUSHOVER_USER,
                "title": title,
                "message": message,
            },
        )
    except Exception as e:
        raise NotificationException(e)


__all__ = ("notify_pushover", "NotificationException")

if __name__ == '__main__':
    notify_pushover("Test", "Test")
