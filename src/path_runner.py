from runner import *
from network import *

T = 100000 # 100000
S = 16

processes = []

# Zipfs
N = 10
fout = "path_10_z_z.txt"
processes.append(start_simulation(T, N, S, 1, create_path, lambda items : ZipfDistribution(1.3, items), lambda items : ZipfDistribution(1.3, items), 1.0, 0.0, fout))

N = 100
fout = "path_100_z_z.txt"
processes.append(start_simulation(T, N, S, 1, create_path, lambda items : ZipfDistribution(1.3, items), lambda items : ZipfDistribution(1.3, items), 1.0, 0.0, fout))

N = 1000
fout = "path_1000_z_z.txt"
processes.append(start_simulation(T, N, S, 1, create_path, lambda items : ZipfDistribution(1.3, items), lambda items : ZipfDistribution(1.3, items), 1.0, 0.0, fout))
#
# N = 10000
# fout = "path_10000_z_z.txt"
# processes.append(start_simulation(T, N, S, 1, create_path, lambda items : ZipfDistribution(1.3, items), lambda items : ZipfDistribution(1.3, items), 1.0, 0.0, fout))
#
# Zipf real, no knowledge
N = 10
fout = "path_10_z_u.txt"
processes.append(start_simulation(T, N, S, 1, create_path, lambda items : ZipfDistribution(1.3, items), UniformDistribution, 1.0, 0.0, fout))

N = 100
fout = "path_100_z_u.txt"
processes.append(start_simulation(T, N, S, 1, create_path, lambda items : ZipfDistribution(1.3, items), UniformDistribution, 1.0, 0.0, fout))

N = 1000
fout = "path_1000_z_u.txt"
processes.append(start_simulation(T, N, S, 1, create_path, lambda items : ZipfDistribution(1.3, items), UniformDistribution, 1.0, 0.0, fout))
#
# N = 10000
# fout = "path_10000_z_u.txt"
# processes.append(start_simulation(T, N, S, 1, create_path, lambda items : ZipfDistribution(1.3, items), UniformDistribution, 1.0, 0.0, fout))
#
# Randoms
N = 10
fout = "path_10_u_u.txt"
processes.append(start_simulation(T, N, S, 1, create_path, UniformDistribution, UniformDistribution, 1.0, 0.0, fout))

N = 100
fout = "path_100_u_u.txt"
processes.append(start_simulation(T, N, S, 1, create_path, UniformDistribution, UniformDistribution, 1.0, 0.0, fout))

N = 1000
fout = "path_1000_u_u.txt"
processes.append(start_simulation(T, N, S, 1, create_path, UniformDistribution, UniformDistribution, 1.0, 0.0, fout))
#
# N = 10000
# fout = "path_10000_u_u.txt"
# processes.append(start_simulation(T, N, S, 1, create_path, UniformDistribution, UniformDistribution, 1.0, 0.0, fout))

for p in processes:
    p.join()
