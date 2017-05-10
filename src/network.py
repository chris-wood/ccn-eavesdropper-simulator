import networkx
import math
import random
import time

from util import *
from cache import *
from packet import *
from observer import *
from distribution import *
from attack import *

class Node(object):
    def __init__(self, name, caching=True):
        self.name = name
        self.next_hops = {}
        self.neighbors = []

        self.caching = caching
        if caching:
            self.cache = Cache()

    def reset(self):
        if self.caching:
            self.cache.flush()

    def add_link(self, node):
        if node not in self.neighbors:
            self.neighbors.append(node)

    def has_route(self, prefix):
        return prefix in self.next_hops

    def add_route(self, name, node):
        if name not in self.next_hops:
            self.next_hops[name] = [node]
        elif node not in self.next_hops[name]:
            self.next_hops[name].append(node)

    def get_next_hop(self, name, source = None):
        if name in self.next_hops:
            if source == None:
                return self.next_hops[name]
            else:
                neighbors = self.next_hops[name]
                if source in neighbors:
                    neighbors.remove(source)
                return neighbors
        raise Exception("Neighbor not found")

    def get_neighbors(self, to_remove = []):
        copy = self.neighbors[:]
        for other in to_remove:
            if other in copy:
                copy.remove(other)
        return copy

    def process_packet(self, packet, path = []):
        if self.caching:
            # indexing the cache does not include the routable prefix
            identity = self.cache.lookup(packet.identity)
            if identity != None: # and packet.prefix == response.prefix:
                response_packet = Packet(packet.prefix, identity)
                response_packet.hop_count = packet.hop_count
                return response_packet

        prefix = packet.prefix
        if prefix in self.next_hops:
            next_hops = self.next_hops[prefix]
            random.shuffle(next_hops)
            for neighbor in next_hops: # try each face *in random order*
                if neighbor not in path:

                    copy = path[:]
                    copy.append(neighbor)
                    response = neighbor.process_packet(packet.forward(), copy)

                    if response != None:
                        if self.caching:
                            self.cache.add(response.identity, response.identity)
                        return response
            raise Exception("This cannot happen. A content object must be returned: %s %s %s" % (self.name, packet.name, str(path)))
        else:
            raise Exception("We have no route to get this item: %s %s %s %s" % (self.name, packet.name, str(path), str(self.next_hops)))

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.name == other.name
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        next_hops = []
        for prefix in self.next_hops:
            hops = []
            for node in self.next_hops[prefix]:
                hops.append(node.name)
            next_hops.append("%s -> [%s]" % (prefix, ",".join(hops)))
        return "%s %s" % (self.name, next_hops)

    def __repr__(self):
        return str(self)

class ObserverNode(Node):
    def __init__(self, name):
        Node.__init__(self, name)
        self.observer = Observer()

    def reset(self):
        self.observer.reset()

    def process_packet(self, packet, path = []):
        self.observer.add(packet.identity, packet.nonce)
        return Node.process_packet(self, packet, path)

    def get_observer(self):
        return self.observer

class ConsumerNode(Node):
    def __init__(self, name):
        Node.__init__(self, name, False)

    def process_packet(self, packet, path = []):
        result = Node.process_packet(self, packet, path)
        if result == None:
            raise Exception("Consumer failed to fetch content -- routing and forwarding error.")
        return result

class ObservingConsumerNode(Node):
    def __init__(self, name, universe):
        Node.__init__(self, name, False)
        self.universe = universe
        self.hits = {item: 0 for item in universe}

    def process_packet(self, packet, path = []):
        result = Node.process_packet(self, packet, path)
        if result == None:
            raise Exception("Consumer failed to fetch content -- routing and forwarding error.")
        if result.cache_hit:
            self.hits[result.identity] += 1
        return result

    def create_observer(self):
        observer = Observer()
        observer.counts = self.hits
        observer.min_count = min(self.hits.itervalues())
        observer.max_count = max(self.hits.itervalues())
        return observer

class ProducerNode(Node):
    def __init__(self, name, prefix, cache):
        Node.__init__(self, name)
        self.cache = cache
        self.prefix = prefix

    def get_prefix(self):
        return self.prefix

    def process_packet(self, packet, path = []):
        response = self.cache.lookup(packet.identity)
        if response != None: # the prefix may not match
            return Packet(packet.prefix, packet.identity, packet.hop_count)
        return Node.process_packet(self, packet, path)

class Network(object):
    def __init__(self, name):
        self.name = name
        self.nodes = {}
        self.consumers = {}
        self.estimators = {}
        self.producers = {}
        self.observers = {}
        self.id_root = 0

    def num_nodes(self):
        return len(self.nodes)

    # route distribution -- spanning tree style
    def propogate_route(self, source, prefix, visited = []):
        if visited == []:
           visited.append(source)

        for neighbor in source.get_neighbors(visited):
            if neighbor not in visited and not neighbor.has_route(prefix):
                neighbor.add_route(prefix, source)
                copy = visited[:]
                copy.append(neighbor)
                self.propogate_route(neighbor, prefix, copy)

    def __next_node_id(self):
        self.id_root += 1
        return str(self.id_root)

    def reset(self):
        for node in self.nodes:
            if node not in self.producers: # don't delete producer caches!
                self.nodes[node].reset()

    def create_node(self, caching=True):
        identity = self.__next_node_id()
        node = Node(identity, caching)
        self.nodes[identity] = node
        return node

    def create_observer(self):
        identity = self.__next_node_id()
        node = ObserverNode(identity)
        self.nodes[identity] = node
        self.observers[identity] = node
        return node

    def create_consumer(self):
        identity = self.__next_node_id()
        consumer = ConsumerNode(identity)
        self.nodes[identity] = consumer
        self.consumers[consumer.name] = consumer
        return consumer

    def create_estimator(self, universe):
        identity = self.__next_node_id()
        consumer = ObservingConsumerNode(identity, universe)
        self.nodes[identity] = consumer
        self.estimators[consumer.name] = consumer
        return consumer

    def create_producer(self, prefix, cache):
        identity = self.__next_node_id()
        node = ProducerNode(identity, prefix, cache)
        self.nodes[identity] = node
        self.producers[identity] = node
        return node

    def get_consumers(self):
        return self.consumers.values()

    def get_estimators(self):
        return self.estimators.values()

    def get_producers(self):
        return self.producers.values()

    def merge_observers(self):
        obs = []
        for o in self.observers:
            obs.append(self.observers[o].observer)
        return combine_observers(obs)

    def merge_estimators(self):
        est = []
        for e in self.estimators:
            est.append(self.estimators[e].create_observer())
        return combine_observers(est)

    def link(self, idA, idB):
        idA = idA.name
        idB = idB.name
        if idA in self.nodes and idB in self.nodes:
            nodeA = self.nodes[idA]
            nodeB = self.nodes[idB]
            nodeA.add_link(nodeB)
            nodeB.add_link(nodeA)
        else:
            raise Exception("%s or %s does not exist in this network" % (idA, idB))

    def add_route(self, idA, idB, prefix):
        idA = str(idA)
        idB = str(idB)
        if idA in self.nodes and idB in self.nodes:
            nodeA = self.nodes[idA]
            nodeB = self.nodes[idB]
            nodeA.add_route(prefix, nodeB)
        else:
            raise Exception("%s or %s does not exist in this network" % (idA, idB))

    def to_dot(self, path):
        lines = []

        G = networkx.Graph()
        seen = []
        queue = [(self.nodes.values()[0], None)]
        while len(queue) > 0:
            curr, prev = queue.pop()
            if curr not in seen:
                seen.append(curr)
                neighbors = curr.get_neighbors([prev])
                for n in neighbors:
                    G.add_edge(curr.name, n.name)
                    queue.append((n, curr))

        dot = networkx.drawing.nx_pydot.write_dot(G, path)

    def __getitem__(self, key):
        return self.nodes[str(key)]

def create_path(items, adv_fraction, cache_fraction, est_fraction, num_consumers, N = 3):
    net = Network("Path-%d-%f-%f" % (N, adv_fraction, cache_fraction))
    curr = net.create_consumer()

    for i in range(N - 2):
        cache = random_flag(cache_fraction)
        adv = random_flag(adv_fraction)
        if adv:
            next_node = net.create_observer()
        else:
            next_node = net.create_node(cache)

        net.link(curr, next_node)
        curr = next_node

    prod = net.create_producer(items[0].prefix, items[0])
    net.link(curr, prod)
    return net

def create_tree(items, levels, k, adv_fraction, cache_fraction):
    net = Network("Tree-%d-%d-%f-%f" % (levels, k, adv_fraction, cache_fraction))

    root = net.create_producer(items)
    prev_level = [root] # first level

    for level in range(levels - 1):
        curr_level = []
        for node in prev_level:
            for i in range(k):
                if random_flag(adv_fraction):
                    next_node = net.create_observer()
                elif level == levels - 1:
                    next_node = net.create_consumer()
                else:
                    next_node = net.create_node(random_flag(cache_fraction))
                net.link(node, next_node)
                curr_level.append(next_node)
        prev_level = curr_level

    return net

def create_lattice_network(cache_list, adv_fraction, cache_fraction, est_fraction, num_consumers):
    net = Network("Lattice-%d-%d-%f-%f" % (len(cache_list), num_consumers, adv_fraction, cache_fraction))

    producers = []
    consumers = []
    routers = []

    # Create the producers
    for cache in cache_list:
        producer = net.create_producer(cache.prefix, cache)
        producers.append(producer)

    # Create the middle routers
    for cache in cache_list:
        if random_flag(adv_fraction):
            router = net.create_observer()
        else:
            router = net.create_node(random_flag(cache_fraction))
        routers.append(router)

    # Connect the upper router
    for i in range(len(cache_list)):
        for j in range(len(cache_list)):
            net.link(producers[i], routers[j])

    universe = set()
    for cache in cache_list:
        for i in range(cache.size()):
            universe.add(cache.index(i))

    # Create the consumers
    consumer_limit = int(math.ceil(float(num_consumers) / len(routers)))
    router = 0
    index = 0
    for i in range(num_consumers):
        consumer = None
        if random_flag(est_fraction):
            consumer = net.create_estimator(universe)
        else:
            consumer = net.create_consumer()

        net.link(consumer, routers[index])
        router += 1
        if router == consumer_limit:
            index += 1
            router = 0

    return net

def create_att_network(cache_list, adv_fraction, cache_fraction, est_fraction, group_size = 10):
    net = Network("ATT-%d-%f-%f" % (group_size, adv_fraction, cache_fraction))

    number_routers = 42
    routers = []

    # Create the routers
    for i in range(number_routers):
        if random_flag(adv_fraction):
            router = net.create_observer()
        else:
            router = net.create_node(random_flag(cache_fraction))
        routers.append(router)

    # Connect the consumers to edge routers
    edge_routers = [0, 36, 37, 9, 38, 13, 16, 20, 18, 28, 21, 24, 26, 35, 34, 33]
    for r in edge_routers:
        for i in range(group_size):
            consumer = net.create_consumer()
            router = routers[r]
            net.link(consumer, router)

    # Create the producer and connect to R0
    router_index = 0
    for cache in cache_list:
        producer = net.create_producer(cache)
        root = routers[router_index]
        net.link(producer, root)
        router_index = (router_index + 1) % len(routers)

    # Connect the internal routers
    internal_edges = [
        (0, 1),
        (1, 2),
        (1, 17),
        (2, 3),
        (2, 4),
        (2, 6),
        (2, 36),
        (2, 8),
        (2, 17),
        (2, 19),
        (3, 5),
        (4, 16),
        (5, 8),
        (6, 7),
        (6, 37),
        (7, 10),
        (8, 9),
        (8, 11),
        (8, 17),
        (10, 11),
        (11, 16),
        (11, 38),
        (11, 12),
        (11, 13),
        (11, 23),
        (12, 13),
        (13, 23),
        (14, 16),
        (14, 15),
        (15, 39),
        (15, 17),
        (16, 17),
        (16, 19),
        (17, 18),
        (17, 19),
        (17, 29),
        (17, 32),
        (17, 31),
        (17, 39),
        (19, 20),
        (19, 27),
        (21, 22),
        (22, 40),
        (22, 23),
        (22, 25),
        (23, 24),
        (25, 27),
        (26, 27),
        (27, 40),
        (27, 30),
        (27, 31),
        (28, 29),
        (29, 30),
        (30, 31),
        (30, 41),
        (30, 35),
        (31, 41),
        (31, 32),
        (31, 34),
        (32, 33)
    ]

    for (u, v) in internal_edges:
        net.link(routers[u], routers[v])

    return net

def create_edge_dfn_network(cache_list, adv_fraction, cache_fraction, est_fraction, group_size = 1):
    net = Network("DFN-%d-%f-%f" % (group_size, adv_fraction, cache_fraction))

    outRouterIndices = [0, 1, 2, 3, 5, 6, 8, 10, 11, 12, 17, 18, 20, 24, 26, 28, 29]
    num_out_routers = len(outRouterIndices)
    inRouterIndices = [4, 7, 9, 13, 14, 15, 16, 19, 21, 22, 23, 25, 27]

    routers = []
    num_routers = 30
    for i in range(num_routers):
        is_adv = random_flag(adv_fraction)
        if i in outRouterIndices and is_adv:
            router = net.create_observer()
        else:
            router = net.create_node(random_flag(cache_fraction))
        routers.append(router)

    # Connecting consumers to edge routers
    for r in outRouterIndices:
        for i in range(group_size):
            consumer = net.create_consumer()
            router = routers[r]
            net.link(consumer, router)

    # Create the producer and connect to R0
    router_index = 0
    for cache in cache_list:
        producer = net.create_producer(cache.prefix, cache)
        root = routers[outRouterIndices[router_index]]
        net.link(root, producer)
        router_index = (router_index + 1) % num_out_routers

    # Connect the inner routers
    net.link(routers[0], routers[9])
    net.link(routers[1], routers[15])
    net.link(routers[2], routers[9])
    net.link(routers[3], routers[4])
    net.link(routers[4], routers[7])
    net.link(routers[4], routers[14])
    net.link(routers[4], routers[9])
    net.link(routers[4], routers[16])
    net.link(routers[4], routers[25])
    net.link(routers[5], routers[13])
    net.link(routers[6], routers[7])
    net.link(routers[7], routers[9])
    net.link(routers[7], routers[14])
    net.link(routers[7], routers[22])
    net.link(routers[7], routers[23])
    net.link(routers[8], routers[9])
    net.link(routers[9], routers[13])
    net.link(routers[9], routers[14])
    net.link(routers[9], routers[22])
    net.link(routers[9], routers[25])
    net.link(routers[9], routers[27])
    net.link(routers[10], routers[14])
    net.link(routers[11], routers[13])
    net.link(routers[12], routers[13])
    net.link(routers[13], routers[14])
    net.link(routers[13], routers[22])
    net.link(routers[13], routers[25])
    net.link(routers[13], routers[27])
    net.link(routers[14], routers[15])
    net.link(routers[14], routers[18])
    net.link(routers[14], routers[19])
    net.link(routers[15], routers[16])
    net.link(routers[15], routers[19])
    net.link(routers[15], routers[21])
    net.link(routers[15], routers[22])
    net.link(routers[15], routers[23])
    net.link(routers[15], routers[25])
    net.link(routers[15], routers[27])
    net.link(routers[16], routers[23])
    net.link(routers[16], routers[27])
    net.link(routers[17], routers[23])
    net.link(routers[19], routers[22])
    net.link(routers[20], routers[25])
    net.link(routers[21], routers[22])
    net.link(routers[21], routers[27])
    net.link(routers[22], routers[23])
    net.link(routers[22], routers[28])
    net.link(routers[22], routers[29])
    net.link(routers[23], routers[24])
    net.link(routers[23], routers[25])
    net.link(routers[23], routers[27])
    net.link(routers[26], routers[27])

    return net

def create_dfn_network(cache_list, adv_fraction, cache_fraction, est_fraction, group_size = 1):
    net = Network("DFN-%d-%f-%f" % (group_size, adv_fraction, cache_fraction))

    outRouterIndices = [0, 1, 2, 3, 5, 6, 8, 10, 11, 12, 17, 18, 20, 24, 26, 28, 29]
    num_out_routers = len(outRouterIndices)
    inRouterIndices = [4, 7, 9, 13, 14, 15, 16, 19, 21, 22, 23, 25, 27]

    routers = []
    num_routers = 30
    for i in range(num_routers):
        if random_flag(adv_fraction):
            router = net.create_observer()
        else:
            router = net.create_node(random_flag(cache_fraction))
        routers.append(router)

    # Connecting consumers to edge routers
    for r in outRouterIndices:
        for i in range(group_size):
            consumer = net.create_consumer()
            router = routers[r]
            net.link(consumer, router)

    # Create the producer and connect to R0
    router_index = 0
    for cache in cache_list:
        producer = net.create_producer(cache.prefix, cache)
        root = routers[outRouterIndices[router_index]]
        net.link(producer, root)
        router_index = (router_index + 1) % num_out_routers

    # Connect the inner routers
    net.link(routers[0], routers[9])
    net.link(routers[1], routers[15])
    net.link(routers[2], routers[9])
    net.link(routers[3], routers[4])
    net.link(routers[4], routers[7])
    net.link(routers[4], routers[14])
    net.link(routers[4], routers[9])
    net.link(routers[4], routers[16])
    net.link(routers[4], routers[25])
    net.link(routers[5], routers[13])
    net.link(routers[6], routers[7])
    net.link(routers[7], routers[9])
    net.link(routers[7], routers[14])
    net.link(routers[7], routers[22])
    net.link(routers[7], routers[23])
    net.link(routers[8], routers[9])
    net.link(routers[9], routers[13])
    net.link(routers[9], routers[14])
    net.link(routers[9], routers[22])
    net.link(routers[9], routers[25])
    net.link(routers[9], routers[27])
    net.link(routers[10], routers[14])
    net.link(routers[11], routers[13])
    net.link(routers[12], routers[13])
    net.link(routers[13], routers[14])
    net.link(routers[13], routers[22])
    net.link(routers[13], routers[25])
    net.link(routers[13], routers[27])
    net.link(routers[14], routers[15])
    net.link(routers[14], routers[18])
    net.link(routers[14], routers[19])
    net.link(routers[15], routers[16])
    net.link(routers[15], routers[19])
    net.link(routers[15], routers[21])
    net.link(routers[15], routers[22])
    net.link(routers[15], routers[23])
    net.link(routers[15], routers[25])
    net.link(routers[15], routers[27])
    net.link(routers[16], routers[23])
    net.link(routers[16], routers[27])
    net.link(routers[17], routers[23])
    net.link(routers[19], routers[22])
    net.link(routers[20], routers[25])
    net.link(routers[21], routers[22])
    net.link(routers[21], routers[27])
    net.link(routers[22], routers[23])
    net.link(routers[22], routers[28])
    net.link(routers[22], routers[29])
    net.link(routers[23], routers[24])
    net.link(routers[23], routers[25])
    net.link(routers[23], routers[27])
    net.link(routers[26], routers[27])

    return net

def create_random_network(items, n, p, adv_fraction, cache_fraction):
    # https://networkx.github.io/documentation/development/reference/generators.html
    G = networkx.fast_gnp_random_graph(n, p)
    net = Network()

    # Pull off the root
    root = net.create_producer()

    seen = set()
    queue = [(0, root)]
    while len(queue) > 0:
        identity, curr = queue.pop()
        if identity not in seen:
            seen.add(identity)
            neighbors = G.neighbors(identity)
            for n in neighbors:
                if random_flag(adv_fraction):
                    next_node = net.create_observer()
                else:
                    next_node = net.create_node(random_flag(cache_fraction))
                net.link(curr, next_node)
                queue.append((n, next_node))

    return net

def create_simple_graph():
    net = Network()
    nA = net.create_consumer()
    nB = net.create_node(False)
    nC = net.create_observer()
    nD = net.create_producer(items)

    net.link(1, 2)
    net.link(2, 3)
    net.link(3, 4)

    return net
