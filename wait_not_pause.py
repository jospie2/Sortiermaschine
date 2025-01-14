import time

class SetWait:
    def __init__(self, delay: int, seconds : bool = False) -> None:
        self.time = delay * 1000 if seconds else delay
        self.start_time = time.monotonic()

    def time_up(self) -> bool:
        return (time.monotonic() - self.start_time)*1000 >= self.time