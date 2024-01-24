#!/usr/bin/env python3
"""
    Module for web cache and tracker
"""
import typing
import requests_html
from functools import wraps
import redis
import requests


def counting(method: typing.Callable):
    """
    Counts  calls to input method
    """

    @wraps(method)
    def count(self, url: str, *args, **kwargs) -> typing.Callable:
        """
        Caches counts of visits to url
        """
        key = 'count:' + url
        self._redis.incr(key)
        self._redis.expire(key, 10)
        return counting(url, *args, **kwargs)
    return count


class Cache:
    """
    This class queries a webpage and monitors number of visits to it
    """

    def __init__(self):
        """
        Initialise class
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @counting
    def get_page(self, url: str) -> str:
        """
        This function ses the requests module to obtain
        """
        response = requests.get(url)
        return response.text


if __name__ == '__main__':
    url = 'http://slowwly.robertomurray.co.uk'
    cache = Cache()
    print(cache)
    cache.get_page(url)
