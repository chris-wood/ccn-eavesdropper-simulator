class HistogramItem(object):
    def __init__(self, count, item):
        self.count = count
        self.item = item

class Histogram(object):
    def __init__(self):
        self.counts = []

    def add(self, count, item):
        self.counts.append(HistogramItem(count, item))

    def sort(self):
        is_sorted = False
        while not is_sorted:
            is_sorted = True
            for i in range(0, len(self.counts) - 1):
                a = self.counts[i]
                b = self.counts[i + 1]
                if a.count < b.count:
                    self.counts[i], self.counts[i + 1] = b, a
                    is_sorted = False

def distance(choices, actual):
    assert len(choices) == len(actual)
    assert len(choices) > 0

    dist = 0
    for i in range(len(choices)):
        num = (choices[i] - actual[i]) ** 2
        den = choices[i] + actual[i]
        dist += (float(num) / float(den))
    return dist

def advantage(choices, actual):
    assert len(choices) == len(actual)
    assert len(choices) > 0
    match_vector = map(lambda (x, y): x == y, zip(choices, actual))
    num_matches = sum(match_vector)
    total = len(choices)
    adv = float(num_matches) / float(total)
    return num_matches, total, adv

def sort_histogram(hist):
    is_sorted = False
    while not is_sorted:
        is_sorted = True
        for i in range(0, len(hist) - 1):
            a = hist[i]
            b = hist[i + 1]
            if a[0] < b[0]:
                hist[i], hist[i + 1] = b, a
                is_sorted = False
    return hist

class AttackResults(object):
    def __init__(self):
        self.observed_histogram = None
        self.auxiliary_histogram = None
        self.real_histogram = None
        self.sample_size = None
        self.truth_map = None
        self.alpha = None
        self.match_percent = 0.0
        self.cdf = None

def compute_average_match_percent(results):
    percent = 0.0
    for r in results:
        percent += r.match_percent
    return percent / len(results)

def compute_average_cdf(results):
    cdf = map(lambda cdf : cdf[0], results[0].cdf)
    for r in range(1, len(results)):
        result = results[r]
        for i, v in enumerate(cdf):
            cdf[i] += result.cdf[i][0]
    return map(lambda v : v / len(results), cdf)

def freq_attack(observed_hist, aux_hist, real_dist, sample_size):
    # The truth rank is computed from the real distribution
    truth_rank = real_dist.rank()
    truth_map = {}
    for item in truth_rank:
        truth_map[item] = item

    # Sort the histograms
    sort_histogram(aux_hist)
    sort_histogram(observed_hist)

    # Compute alpha, the mapping between the plaintext and ciphertext
    alpha = {} # CT -> PT
    for rank, item in enumerate(observed_hist):
        value = aux_hist[rank][1]
        alpha[item[1]] = value

    # Determine the match percentage
    num_matches = 0
    for item in alpha:
        if alpha[item] == truth_map[item]:
            num_matches += 1
    match_percent = float(num_matches) / len(real_dist.domain())

    # Build the CDF
    cdf = []
    total = 0.0
    matched = 0.0
    for (count, item) in aux_hist:
        did_match = False
        if alpha[item] == truth_map[item]:
            matched += 1.0
            did_match = True
        total += 1.0
        cdf.append((matched / total, did_match))

    # Package up the results
    results = AttackResults()
    results.observed_histogram = observed_hist
    results.auxiliary_histogram = aux_hist
    results.real_histogram = real_dist.histogram(sample_size)
    results.sample_size = sample_size
    results.truth_map = truth_map
    results.alpha = alpha
    results.match_percent = match_percent
    results.cdf = cdf

    return results

def lp_norm_attack(observer, aux_dist, real_dist, sample_size):
    pass
