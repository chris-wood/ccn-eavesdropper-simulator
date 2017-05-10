import sys
import random

from multiprocessing import Process
from cache import *
from network import *

# The number of times each experiment is run
runs = 10

def run_simulation(T, net, prefixes, caches, auxiliary_distribution, request_distribution):
    global runs

    results = []

    cache_indexes = range(len(caches))
    num_consumers = len(net.get_consumers())

    for r in range(runs):
        for t in range(T):
            consumer_index = random_range(0, num_consumers - 1)
            consumer = net.get_consumers()[consumer_index]
            identity, index = request_distribution.sample()

            # This should select a random packet from the request
            # distribution, and then a random prefix from the set of prefixes
            # prefix_index = random_range(0, len(prefixes) - 1)
            # packet = Packet(prefixes[prefix_index], packet.identity)

            random.shuffle(cache_indexes)
            for i in cache_indexes:
                cache = caches[i]
                if cache.lookup(identity):
                    new_packet = Packet(cache.prefix, identity)
                    consumer.process_packet(new_packet)
                    break

        # Collect the observed results, generate the histograms, and then run the attack
        observer = net.merge_observers()
        aux_hist = auxiliary_distribution.histogram(T)
        observed_hist = observer.histogram(request_distribution.domain())

        # print aux_hist
        # print observed_hist

        result = freq_attack(observed_hist, aux_hist, request_distribution, T)
        results.append(result)

    return results

def create_network(net_functor, distributed_caches, adv_p, cache_p, num_consumers = 10):
    net = net_functor(distributed_caches, adv_p, cache_p, 0.0, num_consumers)
    for producer in net.get_producers():
        # print >> sys.stderr, "Propagating %s from %s" % (producer.get_prefix(), producer.name)
        net.propogate_route(producer, producer.get_prefix())

    # net.to_dot(data_prefix(params_to_id(T, N, S, P)) + ".dot")
    # net.to_dot("net_%f_%f_%d.dot" % (adv_p, cache_p, num_consumers))
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
        distributed_caches = content_universe.replicate(prefixes)
    else:
        distributed_caches = [content_universe]

    return distributed_caches, content_universe

def create_prefixes(P):
    prefixes = []
    for i in range(P):
        prefixes.append("prefix-%d" % i)
    return prefixes

def simulate(T, N, S, P, C, content_func, net_func, request_func, aux_func, adv_p, cache_p, output):
    prefixes = create_prefixes(P)

    distributed_caches, universe = content_func(prefixes, N, S)
    net = create_network(net_func, distributed_caches, adv_p, cache_p, C)

    aux_dist = aux_func(universe)
    request_dist = request_func(universe)

    results = run_simulation(T, net, prefixes, distributed_caches, aux_dist, request_dist)

    distance = kolmogorov_smirnov(request_dist, aux_dist)
    mp = compute_average_match_percent(results)
    cdf = compute_average_cdf(results)

    with open(output, "w") as fh:
        fh.write(str(distance))
        fh.write("\n")
        fh.write(str(mp))
        fh.write("\n")
        fh.write(str(cdf))
        fh.write("\n")

    return distance, mp, cdf

def create_simulation(T, N, S, P, net_func, request_func, aux_func, adv_p, cache_p, output, C = 10):
    p = Process(target=simulate, args=(T, N, S, P, C, create_content_split, net_func, request_func, aux_func, adv_p, cache_p, output))
    return p

def start_simulation(T, N, S, P, net_func, request_func, aux_func, adv_p, cache_p, output, C = 10):
    p = Process(target=simulate, args=(T, N, S, P, C, create_content_split, net_func, request_func, aux_func, adv_p, cache_p, output))
    p.start()
    return p

def create_split_simulation(T, N, S, P, net_func, request_func, aux_func, adv_p, cache_p, output, C = 10):
    p = Process(target=simulate, args=(T, N, S, P, C, create_content_split, net_func, request_func, aux_func, adv_p, cache_p, output))
    return p

def start_split_simulation(T, N, S, P, net_func, request_func, aux_func, adv_p, cache_p, output, C = 10):
    p = create_split_simulation(T, N, S, P, C, net_func, request_func, aux_func, adv_p, cache_p, output, C)
    p.start()
    return p

def create_replicate_simulation(T, N, S, P, net_func, request_func, aux_func, adv_p, cache_p, output, C = 10):
    p = Process(target=simulate, args=(T, N, S, P, C, create_content_replicate, net_func, request_func, aux_func, adv_p, cache_p, output))
    return p

def start_replicate_simulation(T, N, S, P, net_func, request_func, aux_func, adv_p, cache_p, output, C = 10):
    p = create_replicate_simulation(T, N, S, P, C, create_content_replicate, net_func, request_func, aux_func, adv_p, cache_p, output)
    p.start()
    return p
