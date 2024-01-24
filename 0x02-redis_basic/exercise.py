#!/usr/bin/env python3
"""
Module declares a redis class and methods
"""
import redis
from uuid import uuid4
from typing import Union, Callable, Optional
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """function that count how many times methods of Cache class are called"""

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
    """Function that store history of inputs and outputs for particular function"""

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
    if method is None or not hasattr(method, '__self__'):
        return
    s_redis = getattr(method.__self__, '_redis', None)
    if not isinstance(s_redis, redis.Redis):
        return
    method_name = method.__qualname__
    input_key = "{}:inputs".format(method_name)
    output_key = "{}:outputs".format(method_name)
    count_call = 0
    if s_redis.exists(method_name) != 0:
        count_call = int(s_redis.get(method_name))

    print("{} was called {} times:".format(method_name, count_call))
    fn_inputs = s_redis.lrange(input_key, 0, -1)
    fn_outputs = s_redis.lrange(output_key, 0, -1)
    for fn_input, fn_output in zip(fn_inputs, fn_outputs):
        print("{}(*{}) -> {}".format(method_name, f(fn_input), f(fn_output)))


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
            function store history of inputs and outputs for particular function
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
