import asyncio
from collections import deque
from engine.settings import ASYNC_MAX_CONCURRENCE


class AsyncioPool:
    def __init__(self, print_status=False):
        """
        @param loop: asyncio loop
        @param concurrency: Maximum number of concurrently running tasks
        """        
        self.__loop = asyncio.new_event_loop()
        self.__concurrency = ASYNC_MAX_CONCURRENCE
        self.__coros = deque([])  # All coroutines queued for execution
        self.__futures = []  # All currently running coroutines
        self.__print_status = print_status

    def add(self, coro):
        """
        @param coro: coroutine to add
        """
        self.__coros.append(coro)
        if self.__print_status:
            self.print_status()

    def run(self):
        if self.__concurrency > 0:
            self.__loop.run_until_complete(self.__wait_for_futures())
        else:
            self.__loop.run_until_complete(self.__no_wait_coros())

    def print_status(self):
        print(" Status: coros:%s - futures:%s" % (len(self.__coros), len(self.__futures)))

    def __start_futures(self):
        self.__concurrency = len(self.__coros) if self.__concurrency >= len(self.__coros) else self.__concurrency
        num_to_start = self.__concurrency - len(self.__futures)
        num_to_start = min(num_to_start, len(self.__coros))

        for _ in range(num_to_start):
            coro = self.__coros.popleft()
            future = asyncio.ensure_future(coro)
            self.__futures.append(future)

            if self.__print_status:
                self.print_status()

    async def __no_wait_coros(self):
        while len(self.__coros) > 0:
            coro = self.__coros.popleft()
            asyncio.ensure_future(coro)

            if self.__print_status:
                self.print_status()

    async def __wait_for_futures(self):
        while len(self.__coros) > 0 or len(self.__futures) > 0:
            self.__start_futures()

            futures_completed, futures_pending = await asyncio.wait(
                self.__futures, return_when=asyncio.FIRST_COMPLETED
            )

            for future in futures_completed:
                self.__futures.remove(future)
           
