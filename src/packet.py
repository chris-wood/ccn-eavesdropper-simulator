from util import *

class Packet(object):
    def __init__(self, prefix, identity, hop_count = 0):
        self.identity = identity
        self.nonce = random_string(8)
        self.update_prefix(prefix)
        self.hop_count = hop_count
        self.cache_hit = False

    def update_prefix(self, prefix):
        self.prefix = prefix
        self.name = prefix + "/" + self.identity

    def copy(self):
        packet = Packet(self.prefix, self.identity, self.hop_count)
        return packet

    def forward(self):
        other = self.copy()
        other.hop_count += 1
        return other

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self)
