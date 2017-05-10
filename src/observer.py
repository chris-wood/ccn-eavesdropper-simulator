from random import shuffle

class Observer(object):
    def __init__(self):
        self.counts = {}
        self.items = []
        self.min_count = 0
        self.max_count = 0

    def reset(self):
        self.min_count = 0
        self.max_count = 0
        self.counts = {}

    def add(self, key, nonce):
        self.items.append((key, nonce))

    def frequency(self, key):
        if key not in self.counts:
            return 0
        return self.counts[key]

    def histogram(self, domain):
        counts = {}
        for d in domain:
            key = str(d)
            count = 0
            if key in self.counts:
                count = self.counts[key]

            item = (count, d)
            if count in counts:
                counts[count].append(item)
            else:
                counts[count] = [item]

        # Shuffle each item with the same count to emulate a random choice between them
        for c in counts:
            shuffle(counts[c])

        final_counts = []
        for c in counts:
            for item in counts[c]:
                final_counts.append(item)

        return final_counts

    def rank(self, aux_rank): # {item} -> count
        ranked = []

        aux_index = 0
        count = self.max_count
        while count >= 0:
            for key in self.counts:
                if self.counts[key] == count:
                    ranked.append(aux_rank[aux_index])
                    aux_index += 1
            count -= 1

        tail = aux_rank[aux_index:]
        tail.shuffle()
        ranked.extend(tail)

        return map(lambda l : l, ranked)

    def __str__(self):
        return str(self.counts)

    def __repr__(self):
        return str(self)

def combine_observers(observers):
    nonces = {}
    results = {}
    min_count = 10 ** 10
    max_count = 0

    for observer in observers:
        for (item, nonce) in observer.items:
            if item not in nonces:
                nonces[item] = [nonce]
                if item not in results:
                    results[item] = 1
                else:
                    results[item] += 1
            elif item in nonces and nonce not in nonces[item]:
                nonces[item].append(nonce)
                if item not in results:
                    results[item] = 1
                else:
                    results[item] += 1

    for item in results:
        count = results[item]
        min_count = count if count < min_count else min_count
        max_count = count if count > max_count else max_count

    observer = Observer()
    observer.counts = results
    observer.min_count = min_count
    observer.max_count = max_count

    return observer
