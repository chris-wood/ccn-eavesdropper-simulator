from runner import *
from network import *

def run_simulations(T, N, adv_split):
    S = 16
    processes = []

    # Caching split, single producer
    # fout = "dfn_half_single_u_u_%d_%f.txt" % (N, adv_split)
    # processes.append(start_simulation(T, N, S, 1, create_dfn_network, UniformDistribution, UniformDistribution, adv_split, 0.5, fout))
    # fout = "dfn_half_single_z_u_%d_%f.txt" % (N, adv_split)
    # processes.append(start_simulation(T, N, S, 1, create_dfn_network, lambda items : ZipfDistribution(1.3, items), UniformDistribution, adv_split, 0.5, fout))
    fout = "dfn_half_single_z_z_%d_%f.txt" % (N, adv_split)
    processes.append(start_simulation(T, N, S, 1, create_dfn_network, lambda items : ZipfDistribution(1.3, items), lambda items : ZipfDistribution(1.3, items), adv_split, 0.5, fout))

    # Caching everywhere, single producer,
    # fout = "dfn_all_single_u_u_%d_%f.txt" % (N, adv_split)
    # processes.append(start_simulation(T, N, S, 1, create_dfn_network, UniformDistribution, UniformDistribution, adv_split, 1.0, fout))
    # fout = "dfn_all_single_z_u_%d_%f.txt" % (N, adv_split)
    # processes.append(start_simulation(T, N, S, 1, create_dfn_network, lambda items : ZipfDistribution(1.3, items), UniformDistribution, adv_split, 1.0, fout))
    fout = "dfn_all_single_z_z_%d_%f.txt" % (N, adv_split)
    processes.append(start_simulation(T, N, S, 1, create_dfn_network, lambda items : ZipfDistribution(1.3, items), lambda items : ZipfDistribution(1.3, items), adv_split, 1.0, fout))

    # Caching nowhere, single producer
    # fout = "dfn_none_single_u_u_%d_%f.txt" % (N, adv_split)
    # processes.append(start_simulation(T, N, S, 1, create_dfn_network, UniformDistribution, UniformDistribution, adv_split, 0.0, fout))
    # fout = "dfn_none_single_z_u_%d_%f.txt" % (N, adv_split)
    # processes.append(start_simulation(T, N, S, 1, create_dfn_network, lambda items : ZipfDistribution(1.3, items), UniformDistribution, adv_split, 0.0, fout))
    fout = "dfn_none_single_z_z_%d_%f.txt" % (N, adv_split)
    processes.append(start_simulation(T, N, S, 1, create_dfn_network, lambda items : ZipfDistribution(1.3, items), lambda items : ZipfDistribution(1.3, items), adv_split, 0.0, fout))

    return processes

def run_edge_simulations(T, N, adv_split):
    S = 16
    processes = []

    # Caching split, single producer
    # fout = "dfn_edge_half_single_u_u_%d_%f.txt" % (N, adv_split)
    # processes.append(start_simulation(T, N, S, 1, create_edge_dfn_network, UniformDistribution, UniformDistribution, adv_split, 0.5, fout))
    # fout = "dfn_edge_half_single_z_u_%d_%f.txt" % (N, adv_split)
    # processes.append(start_simulation(T, N, S, 1, create_edge_dfn_network, lambda items : ZipfDistribution(1.3, items), UniformDistribution, adv_split, 0.5, fout))
    fout = "dfn_edge_half_single_z_z_%d_%f.txt" % (N, adv_split)
    processes.append(start_simulation(T, N, S, 1, create_edge_dfn_network, lambda items : ZipfDistribution(1.3, items), lambda items : ZipfDistribution(1.3, items), adv_split, 0.5, fout))

    # Caching everywhere, single producer,
    # fout = "dfn_edge_all_single_u_u_%d_%f.txt" % (N, adv_split)
    # processes.append(start_simulation(T, N, S, 1, create_edge_dfn_network, UniformDistribution, UniformDistribution, adv_split, 1.0, fout))
    # fout = "dfn_edge_all_single_z_u_%d_%f.txt" % (N, adv_split)
    # processes.append(start_simulation(T, N, S, 1, create_edge_dfn_network, lambda items : ZipfDistribution(1.3, items), UniformDistribution, adv_split, 1.0, fout))
    fout = "dfn_edge_all_single_z_z_%d_%f.txt" % (N, adv_split)
    processes.append(start_simulation(T, N, S, 1, create_edge_dfn_network, lambda items : ZipfDistribution(1.3, items), lambda items : ZipfDistribution(1.3, items), adv_split, 1.0, fout))

    # Caching nowhere, single producer
    # fout = "dfn_edge_none_single_u_u_%d_%f.txt" % (N, adv_split)
    # processes.append(start_simulation(T, N, S, 1, create_edge_dfn_network, UniformDistribution, UniformDistribution, adv_split, 0.0, fout))
    # fout = "dfn_edge_none_single_z_u_%d_%f.txt" % (N, adv_split)
    # processes.append(start_simulation(T, N, S, 1, create_edge_dfn_network, lambda items : ZipfDistribution(1.3, items), UniformDistribution, adv_split, 0.0, fout))
    fout = "dfn_edge_none_single_z_z_%d_%f.txt" % (N, adv_split)
    processes.append(start_simulation(T, N, S, 1, create_edge_dfn_network, lambda items : ZipfDistribution(1.3, items), lambda items : ZipfDistribution(1.3, items), adv_split, 0.0, fout))

    return processes

def run_distributed_split_simulations(T, N, adv_split):
    S = 16
    processes = []

    # Caching split, split producer
    # fout = "dfn_half_split_u_u_%d_%f.txt" % (N, adv_split)
    # processes.append(start_split_simulation(T, N, S, 2, create_dfn_network, UniformDistribution, UniformDistribution, adv_split, 0.5, fout))
    # fout = "dfn_half_split_z_u_%d_%f.txt" % (N, adv_split)
    # processes.append(start_split_simulation(T, N, S, 2, create_dfn_network, lambda items : ZipfDistribution(1.3, items), UniformDistribution, adv_split, 0.5, fout))
    fout = "dfn_half_split_z_z_%d_%f.txt" % (N, adv_split)
    processes.append(start_split_simulation(T, N, S, 2, create_dfn_network, lambda items : ZipfDistribution(1.3, items), lambda items : ZipfDistribution(1.3, items), adv_split, 0.5, fout))

    # Caching everywhere, split producer
    # fout = "dfn_all_split_u_u_%d_%f.txt" % (N, adv_split)
    # processes.append(start_split_simulation(T, N, S, 2, create_dfn_network, UniformDistribution, UniformDistribution, adv_split, 1.0, fout))
    # fout = "dfn_all_split_z_u_%d_%f.txt" % (N, adv_split)
    # processes.append(start_split_simulation(T, N, S, 2, create_dfn_network, lambda items : ZipfDistribution(1.3, items), UniformDistribution, adv_split, 1.0, fout))
    fout = "dfn_all_split_z_z_%d_%f.txt" % (N, adv_split)
    processes.append(start_split_simulation(T, N, S, 2, create_dfn_network, lambda items : ZipfDistribution(1.3, items), lambda items : ZipfDistribution(1.3, items), adv_split, 1.0, fout))

    # Caching nowhere, split producer
    # fout = "dfn_none_split_u_u_%d_%f.txt" % (N, adv_split)
    # processes.append(start_split_simulation(T, N, S, 2, create_dfn_network, UniformDistribution, UniformDistribution, adv_split, 0.0, fout))
    # fout = "dfn_none_split_z_u_%d_%f.txt" % (N, adv_split)
    # processes.append(start_split_simulation(T, N, S, 2, create_dfn_network, lambda items : ZipfDistribution(1.3, items), UniformDistribution, adv_split, 0.0, fout))
    fout = "dfn_none_split_z_z_%d_%f.txt" % (N, adv_split)
    processes.append(start_split_simulation(T, N, S, 2, create_dfn_network, lambda items : ZipfDistribution(1.3, items), lambda items : ZipfDistribution(1.3, items), adv_split, 0.0, fout))

    return processes

def run_distributed_replicate_simulations(T, N, adv_split):
    S = 16
    processes = []

    # Caching split, split producer
    # fout = "dfn_half_replicate_u_u_%d_%f.txt" % (N, adv_split)
    # processes.append(start_replicate_simulation(T, N, S, 2, create_dfn_network, UniformDistribution, UniformDistribution, adv_split, 0.5, fout))
    # fout = "dfn_half_replicate_z_u_%d_%f.txt" % (N, adv_split)
    # processes.append(start_replicate_simulation(T, N, S, 2, create_dfn_network, lambda items : ZipfDistribution(1.3, items), UniformDistribution, adv_split, 0.5, fout))
    fout = "dfn_half_replicate_z_z_%d_%f.txt" % (N, adv_split)
    processes.append(start_replicate_simulation(T, N, S, 2, create_dfn_network, lambda items : ZipfDistribution(1.3, items), lambda items : ZipfDistribution(1.3, items), adv_split, 0.5, fout))

    # Caching everywhere, split producer
    # fout = "dfn_all_replicate_u_u_%d_%f.txt" % (N, adv_split)
    # processes.append(start_replicate_simulation(T, N, S, 2, create_dfn_network, UniformDistribution, UniformDistribution, adv_split, 1.0, fout))
    # fout = "dfn_all_replicate_z_u_%d_%f.txt" % (N, adv_split)
    # processes.append(start_replicate_simulation(T, N, S, 2, create_dfn_network, lambda items : ZipfDistribution(1.3, items), UniformDistribution, adv_split, 1.0, fout))
    fout = "dfn_all_replicate_z_z_%d_%f.txt" % (N, adv_split)
    processes.append(start_replicate_simulation(T, N, S, 2, create_dfn_network, lambda items : ZipfDistribution(1.3, items), lambda items : ZipfDistribution(1.3, items), adv_split, 1.0, fout))

    # Caching nowhere, split producer
    # fout = "dfn_none_replicate_u_u_%d_%f.txt" % (N, adv_split)
    # processes.append(start_replicate_simulation(T, N, S, 2, create_dfn_network, UniformDistribution, UniformDistribution, adv_split, 0.0, fout))
    # fout = "dfn_none_replicate_z_u_%d_%f.txt" % (N, adv_split)
    # processes.append(start_replicate_simulation(T, N, S, 2, create_dfn_network, lambda items : ZipfDistribution(1.3, items), UniformDistribution, adv_split, 0.0, fout))
    fout = "dfn_none_replicate_z_z_%d_%f.txt" % (N, adv_split)
    processes.append(start_replicate_simulation(T, N, S, 2, create_dfn_network, lambda items : ZipfDistribution(1.3, items), lambda items : ZipfDistribution(1.3, items), adv_split, 0.0, fout))

    return processes

T = 100
N = 50
adv_split = 0.5

# Random adv
processes = []
# 10
# processes.extend(run_simulations(T, N, 0.5))
# processes.extend(run_simulations(T, N, 0.25))
# processes.extend(run_simulations(T, N, 1.0))
# 100
processes.extend(run_simulations(T, N, 0.5))
processes.extend(run_simulations(T, N, 0.25))
processes.extend(run_simulations(T, N, 1.0))
# 1000
# processes.extend(run_simulations(T, N, 0.5))
# processes.extend(run_simulations(T, N, 0.25))
# processes.extend(run_simulations(T, N, 1.0))
# 10000
# processes.extend(run_simulations(T, N, 0.5))
# processes.extend(run_simulations(T, N, 0.25))
# processes.extend(run_simulations(T, N, 1.0))

# Edge adv
# processes.extend(run_edge_simulations(T, N, 0.5))
# processes.extend(run_edge_simulations(T, N, 0.25))
# processes.extend(run_edge_simulations(T, N, 1.0))
processes.extend(run_edge_simulations(T, N, 0.5))
processes.extend(run_edge_simulations(T, N, 0.25))
processes.extend(run_edge_simulations(T, N, 1.0))

# processes.extend(run_edge_simulations(T, N, 0.5))
# processes.extend(run_edge_simulations(T, N, 0.25))
# processes.extend(run_edge_simulations(T, N, 1.0))
# processes.extend(run_edge_simulations(T, N, 0.5))
# processes.extend(run_edge_simulations(T, N, 0.25))
# processes.extend(run_edge_simulations(T, N, 1.0))

# # processes.extend(run_distributed_split_simulations(T, N, 0.5))
# # processes.extend(run_distributed_split_simulations(T, N, 0.25))
# # processes.extend(run_distributed_split_simulations(T, N, 1.0))
# processes.extend(run_distributed_split_simulations(T, N, 0.5))
# processes.extend(run_distributed_split_simulations(T, N, 0.25))
# processes.extend(run_distributed_split_simulations(T, N, 1.0))
# # processes.extend(run_distributed_split_simulations(T, N, 0.5))
# # processes.extend(run_distributed_split_simulations(T, N, 0.25))
# # processes.extend(run_distributed_split_simulations(T, N, 1.0))
# # processes.extend(run_distributed_split_simulations(T, N, 0.5))
# # processes.extend(run_distributed_split_simulations(T, N, 0.25))
# # processes.extend(run_distributed_split_simulations(T, N, 1.0))

# # processes.extend(run_distributed_replicate_simulations(T, N, 0.5))
# # processes.extend(run_distributed_replicate_simulations(T, N, 0.25))
# # processes.extend(run_distributed_replicate_simulations(T, N, 1.0))
# processes.extend(run_distributed_replicate_simulations(T, N, 0.5))
# processes.extend(run_distributed_replicate_simulations(T, N, 0.25))
# processes.extend(run_distributed_replicate_simulations(T, N, 1.0))
# # processes.extend(run_distributed_replicate_simulations(T, N, 0.5))
# # processes.extend(run_distributed_replicate_simulations(T, N, 0.25))
# # processes.extend(run_distributed_replicate_simulations(T, N, 1.0))
# # processes.extend(run_distributed_replicate_simulations(T, N, 0.5))
# # processes.extend(run_distributed_replicate_simulations(T, N, 0.25))
# # processes.extend(run_distributed_replicate_simulations(T, N, 1.0))

# Wait for them all to finish...
for p in processes:
    p.join()
