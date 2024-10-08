#!/usr/bin/env python3
""" Coroutine with async """

from typing import Generator
import asyncio
import random


async def async_generator() -> Generator[float, None, None]:
    """
    loop 10 times, each time asynchronously wait 1 second,
    then yield a random number between 0 and 10
    """
    for _ in range(10):
        yield random.random()
        await asyncio.sleep(1)
