from cache import *
from util import *
from network import *
from distribution import *
from attack import *

N = 100
T = 100000
S = 16
items = Cache("foo")
items.populate(N, S)

#net = create_tree(items, 4, 2, 1.0, 1.0)
#net = create_random_network(items, 5, 0.5, 1.0, 1.0)
group_size = 10
net = create_dfn_network([items], 1.0, 0.0)
#net = create_att_network(items, 10, 0.5, 1.0)
# net.to_dot("test.dot")

producer = net.get_producers()[0] # just pick the first one
net.propogate_route(producer, producer.prefix)

# https://arxiv.org/pdf/1202.0108.pdf
pop_dist = ZipfDistribution(0.75, items)
aux_dist = pop_dist
# aux_dist = UniformDistribution(items)
#pop_dist = aux_dist

num_consumers = len(net.get_consumers())
counts = {}
for t in range(T):
    consumer_index = random_range(0, num_consumers - 1)
    consumer = net.get_consumers()[consumer_index]

    identity, index = pop_dist.sample()
    if identity not in counts:
        counts[identity] = 0
    counts[identity] += 1
    consumer.process_packet(Packet(producer.prefix, identity))

# print "counts", counts
observer = net.merge_observers()
# print observer.histogram(items.itemize())
results = freq_attack(observer, aux_dist, pop_dist, T)
print results.match_percent
print results.cdf
