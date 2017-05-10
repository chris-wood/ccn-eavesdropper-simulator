from util import *
import random
import sys
import numpy as np
from scipy.stats import zipf
from scipy.stats import norm
from scipy.stats import rv_discrete

def kolmogorov_smirnov(d1, d2):
    e1 = d1.edf()
    e2 = d2.edf()
    delta = map(lambda (x, y) : abs(x - y), zip(e1, e2))
    return max(delta)

class Distribution(object):
    def __init__(self, items):
        self.items = items
        self.num_items = items.size()

    def domain(self):
        items = self.items.itemize()
        return items

    def sample(self):
        pass

    def rank(self):
        pass

    def histogram(self, total_requests):
        pass

    def pmf(self, index):
        pass

    def edf(self):
        return map(lambda i : self.pmf(i), range(self.num_items))

class NormalDistribution(Distribution):
    def __init__(self, items):
        Distribution.__init__(self, items)
        self.mu = items.size() / 2
        self.sigma = 1.0

    def sample(self):
        s = np.random.normal(self.mu, self.sigma)
        index = (int(s) + self.items.size()) % self.items.size()
        return self.items.index(index), index

    def histogram(self, total_requests):
        bins = []
        for i in range(self.items.size()):
            p_i = norm.pdf(i, self.mu, self.sigma)
            count = int(math.ceil(p_i * total_requests))
            bins.append(count)
        return bins

    def rank(self):
        left = []
        right = []
        middle = self.items.size() / 2
        ranked = [self.items.index(middle)]
        for i in range(middle - 1, 0, -1):
            left.append(self.items.index(i))
        for i in range(middle + 1, self.items.size()):
            right.append(self.items.index(i))

        # splice together
        while len(left) > 0 and len(right) > 0:
            ranked.append(left.pop(0))
            ranked.append(right.pop(0))
        while len(left) > 0:
            ranked.append(left.pop(0))
        while len(right) > 0:
            ranked.append(right.pop(0))

        return ranked

    def pmf(self, index):
        return 0.0

class UniformDistribution(Distribution):
    def __init__(self, items):
        Distribution.__init__(self, items)
        self.fraction = 1.0 / float(self.items.size())

    def sample(self):
        i = random_range(0, self.num_items - 1)
        return self.items.index(i), i

    def histogram(self, total_requests):
        fraction = total_requests / self.num_items
        items = self.items.itemize()
        random.shuffle(items)
        hist = []
        for i in items:
            hist.append((fraction, i))
        return hist

    def rank(self):
        items = map(lambda i : i, self.items.itemize())
        random.shuffle(items)
        return items

    def pmf(self, index):
        return self.fraction

    def domain(self):
        items = self.items.itemize()
        random.shuffle(items)
        return items

    def __repr__(self):
        return "uniform-%d" % self.items.size()

class ZipfDistribution(Distribution):
    def __init__(self, alpha, items):
        Distribution.__init__(self, items)
        self.alpha = alpha

        # Initialize the zipf RV from which we will sample
        n = self.items.size()
        x = np.arange(1, n + 1)
        weights = x ** (-1 * self.alpha)
        weights /= weights.sum()
        self.weights = weights
        self.rv = rv_discrete(name="bounded_zipf", values=(x, weights))

        # https://docs.scipy.org/doc/numpy/reference/generated/numpy.random.zipf.html
        # np.random.zipf(alpha, size=None)

    def sample(self):
        i = self.rv.rvs() - 1
        return self.items.index(i), i

    def histogram(self, num_trials):
        items = self.items.itemize()
        hist = []
        for i, d in enumerate(items):
            p = self.weights[i]
            fraction = num_trials * p
            hist.append((fraction, d))
        return hist

    def rank(self):
        return map(lambda i : i, self.items.itemize()) # they're indexed by k, decreasing in popularity

    def pmf(self, index):
        #return self.rv.pmf(index + 1)
        return self.weights[index]

    def __repr__(self):
        return "zipf-%f-%d" % (self.alpha, self.items.size())
