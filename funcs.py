from typing import Set, Dict


class Node:
    def __init__(self, xy):
        self.xy = xy
        self.neighbours = set()


class Bag:
    def __init__(self, data):
        self.set = set(data)

    def try_take(self, item):
        exists = item in self.set
        self.set.discard(item)
        return exists