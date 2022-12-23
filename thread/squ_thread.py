import threading


class SquThread(threading.Thread):
    def __init__(self, index: int, sub_table: list[int]):
        threading.Thread.__init__(self)
        self.index = index
        self.sub_table = sub_table

    def run(self):
        self.sub_table = list(map(self.squ, self.sub_table))
        print(f'thread {self.index}: {self.sub_table}')

        threadLock.acquire()
        table[self.index * 1000: (self.index + 1) * 1000] = self.sub_table
        threadLock.release()

    def squ(self, x: int) -> int:
        return x ** 2


if __name__ == "__main__":
    threadLock = threading.Lock()
    table = [index for index in range(10000)]
    print(f'table {table}')
    threads = [SquThread(index, table[index * 1000:(index + 1) * 1000]) for index in range(10)]
    [thread.start() for thread in threads]
    [thread.join() for thread in threads]
    print(f'table {table}')
    exit()
