#!/usr/bin/env python3
"""
    Module for web cache and tracker
"""
import redis
import requests
s_redis = redis.Redis()
count = 0


def get_page(url: str) -> str:
    """ get a page and cach value"""
    s_redis.set(f"cached:{url}", count)
    resp = requests.get(url)
    s_redis.incr(f"count:{url}")
    s_redis.setex(f"cached:{url}", 10, s_redis.get(f"cached:{url}"))
    return resp.text


if __name__ == "__main__":
    get_page('http://slowwly.robertomurray.co.uk')
