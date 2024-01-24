#!/usr/bin/env python3
"""
Module declares a redis class and methods
"""
import redis
from uuid import uuid4
from typing import Union, Callable, Optional
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """
        function that count how many times methods of Cache class are called
    """

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
            Wrap decorated function
            returns: wrapper
        """
        method_key = method.__qualname__
        self._redis.incr(method_key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """store history of inputs and outputs for particular function"""

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
            Wrap the decorated function
            returns: wrapper
        """
        input = str(args)
        self._redis.rpush(method.__qualname__ + ":inputs", input)
        method_output = str(method(self, *args, **kwargs))
        self._redis.rpush(method.__qualname__ + ":outputs", method_output)
        return method_output
    return wrapper


def replay(method: Callable) -> None:
    """
        Function that replays the history of a particular function
    """
    s_redis = redis.Redis()
    method_key = method.__qualname__
    inp_key = s_redis.lrange("{}:inputs".format(method_key), 0, -1)
    outp_key = s_redis.lrange("{}:outputs".format(method_key), 0, -1)
    call_count = len(inp_key)
    str_time = 'times'
    if call_count == 1:
        str_time = 'time'
    fin = '{} was called {} {}:'.format(method_key, call_count, str_time)
    print(fin)
    for k, v in zip(inp_key, outp_key):
        fin = '{}(*{}) -> {}'.format(
            method_key,
            k.decode('utf-8'),
            v.decode('utf-8')
        )
        print(fin)


class Cache:
    """Function that declares cache redis class"""

    def __init__(self):
        """upon init to store instance of Redis client and flush"""
        self._redis = redis.Redis(host='localhost', port=6379, db=0)
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
            store history of inputs and outputs for particular function
        """
        r_key = str(uuid4())
        self._redis.set(r_key, data)
        return r_key

    def get(self, key: str,
            fn: Optional[Callable] = None) -> Union[str, bytes, int, float]:
        """
            function convert the data back to desired format
        """
        val = self._redis.get(key)
        return val if not fn else fn(val)

    def get_str(self, key: str) -> str:
        """function to get string from cache"""
        val = self._redis.get(key)
        return val.decode("utf-8")

    def get_int(self, key: str) -> int:
        """function to get int from cache"""
        val = self._redis.get(key)
        try:
            val = int(val.decode("utf-8"))
        except Exception:
            val = 0
        return val
