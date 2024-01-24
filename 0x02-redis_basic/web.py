#!/usr/bin/env python3
"""
Module for web cache and tracker
"""
from datetime import timedelta
from typing import Callable
import requests
from functools import wraps
import redis

s_redis = redis.Redis()


def count_url_response(method: Callable):
    """
        Decorator counting how many times URL is accessed
    """

    @wraps(method)
    def invoker(url) -> str:
        '''The wrapper function for caching the output.
        '''
        s_redis.incr(f'count:{url}')
        result = s_redis.get(f'result:{url}')
        if result:
            return result.decode('utf-8')
        result = method(url)
        s_redis.set(f'count:{url}', 0)
        s_redis.setex(f'result:{url}', 10, result)
        return result
    return invoker


@count_url_response
def get_page(url: str) -> str:
    """
        Return HTML content
    """
    return requests.get(url).text
