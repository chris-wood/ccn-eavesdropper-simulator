import sys
import random

from multiprocessing import Process
from cache import *
from network import *
from attack import *

runs = 1

def run_simulation(T, net, prefixes, caches, auxiliary_distribution, request_distribution):
    global runs

    results = []

    cache_indexes = range(len(caches))
    num_consumers = len(net.get_consumers())

    for r in range(runs):
        for t in range(T):
            consumer_index = random_range(0, num_consumers - 1)
            consumer = net.get_consumers()[consumer_index]
            identifier, index = request_distribution.sample()

            # This should select a random packet from the request
            # distribution, and then a random prefix from the set of prefixes
            # prefix_index = random_range(0, len(prefixes) - 1)
            # packet = Packet(prefixes[prefix_index], packet.identity)

            random.shuffle(cache_indexes)
            for i in cache_indexes:
                cache = caches[i]
                if cache.lookup(identifier):
                    packet = Packet(cache.prefix, identifier)
                    consumer.process_packet(packet)
                    break

            # XXX: this is where we want to implement the estimation algorithm *alongside* the normal consumers
            # after a consumer issues an interest, we want to issue an interest and see if there's a hit
            # TODO(cawood)

        # Collect the estimated results
        estimator = net.merge_estimators()
        request_hist = request_distribution.histogram(T)
        estimated_hist = estimator.histogram(request_distribution.domain())

        # Sort and compare the histograms
        sort_histogram(request_hist)
        sort_histogram(estimated_hist)

        print request_hist
        print estimated_hist

        count = 0
        for rank, item in enumerate(estimated_hist):
            if request_hist[rank][1] == item:
                count += 1

        results.append(float(count) / float(T))

    return results

def create_network(net_functor, distributed_caches, adv_p, cache_p, est_p, num_consumers = 10):
    net = net_functor(distributed_caches, adv_p, cache_p, est_p, num_consumers)
    for producer in net.get_producers():
        net.propogate_route(producer, producer.get_prefix())
    return net

def create_content_split(prefixes, N, S):
    content_universe = Cache(prefixes[0])
    content_universe.populate(N, S)
    if len(prefixes) >  1:
        distributed_caches = content_universe.split(prefixes)
    else:
        distributed_caches = [content_universe]

    return distributed_caches, content_universe

def create_content_replicate(prefixes, N, S):
    content_universe = Cache(prefixes[0])
    content_universe.populate(N, S)
    if len(prefixes) >  1:
        distributed_caches = content_universe.split(prefixes)
    else:
        distributed_caches = [content_universe]

    return distributed_caches, content_universe

def create_prefixes(P):
    prefixes = []
    for i in range(P):
        prefixes.append("prefix-%d" % i)
    return prefixes

def simulate(T, N, S, P, C, content_func, net_func, request_func, aux_func, adv_p, cache_p, est_p, output):
    prefixes = create_prefixes(P)

    distributed_caches, universe = content_func(prefixes, N, S)
    net = create_network(net_func, distributed_caches, adv_p, cache_p, est_p, C)

    request_dist = request_func(universe)
    aux_dist = aux_func(universe)

    results = run_simulation(T, net, prefixes, distributed_caches, aux_dist, request_dist)

    print results

Ts = [10000]
Ns = [10] #range(10, 100, 10)
Ps = [1] #range(2, 11)
Cs = [25] #range(25, 101, 25)
S = 16

adv_p = 0.0
cache_p = 1.0
est_p = 0.5
processes = []

for T in Ts:
    for N in Ns:
        for P in Ps:
            for C in Cs:
                fout = "estimate_lattice_%d_%d_%d_%d_%f.txt" % (T, N, P, C, adv_p)
                simulate(T, N, S, P, C, create_content_replicate, create_lattice_network, lambda items : ZipfDistribution(1.3, items), lambda items : ZipfDistribution(1.3, items), adv_p, cache_p, est_p, fout)
