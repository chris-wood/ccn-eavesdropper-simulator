from util import *
from packet import *

class Cache(object):
    def __init__(self, prefix = "", capacity = -1): # negative capacity means boundless to start
        self.cache = {}
        self.lru = {}
        self.capacity = capacity
        self.tm = 0
        self.prefix = prefix
        self.num_items = 0

    def flush(self):
        self.cache = {}
        self.lru = {}
        self.tm = 0
        self.num_items = 0

    def size(self):
        return len(self.cache)

    def populate(self, n, m):
        items = [random_string(m) for i in range(n)]
        for item in items:
            self.cache[item] = item # Packet(self.prefix, item)
        self.num_items = len(self.cache.keys())

    def split(self, split_prefixes):
        num_prefixes = len(split_prefixes)
        split_size = len(self.cache) / num_prefixes

        caches = []
        for i in range(num_prefixes):
            prefix = split_prefixes[i]
            cache = Cache(prefix)
            for n in range(split_size):
                key = self.cache.keys()[n]
                identity = self.cache[key]
                cache.add(identity, identity)
            caches.append(cache)

        return caches

    def replicate(self, replicate_prefixes):
        ''' Create |replicate_prefixes| copies of this cache
        with different prefixes.'''
        num_prefixes = len(replicate_prefixes)
        caches = []
        for i in range(num_prefixes):
            prefix = replicate_prefixes[i]
            cache = Cache(prefix)
            for p in self.cache:
                cache.add(p, p)
            caches.append(cache)

        return caches

    def partition(self, split_prefix, percentage = 0.5):
        split_size = int(len(self.cache) * percentage)
        split_cache = Cache()
        for i in range(split_size):
            packet = self.cache[self.cache.keys()[i]]
            del self.cache[packet]
            self.num_items -= 1

            packet.update_prefix(split_prefix)
            split_cache.add_item(packet)

        return split_cache

    def add(self, name, item):
        if len(self.cache) >= self.capacity and self.capacity > 0:
            old_key = min(self.lru.keys(), key = lambda k : self.lru[k])
            self.cache.pop(old_key)
            self.lru.pop(old_key)
        self.cache[name] = item
        self.lru[name] = self.tm
        self.tm += 1

    def index(self, i):
        if i < 0 or i >= self.size():
            raise Exception("Item index %d out of bounds (limit %d)" % (i, self.size()))
        key = self.cache.keys()[i]
        return self.cache[key]

    def lookup(self, key):
        if key in self.cache:
            self.lru[key] = self.tm
            self.tm += 1
            return self.cache[key]
        return None

    def itemize(self):
        return self.cache.values()

    def random_item(self):
        i = random_range(0, self.size() - 1)
        return self.index(i)

    def __repr__(self):
        return ",".join(map(lambda i : i, self.cache))
