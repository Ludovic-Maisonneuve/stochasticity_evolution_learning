import time

from functions.classes import *
from functions.dynamics import *
from functions.save_and_open import *

## Parameters' value

f_0, s_0 = 5, 1
beta_v, beta_o, alpha = 1.4, 1.3, 0.1
eps, rho = 0.05, 0.05
sigma_v = 0.1
sigma_o = 0.1
sigma_i = 0.025
eta_f, eta_s = 25, 5
theta = 0.1
gamma = 0.01

N_0 = 1
P_mut = 0.01
mutation_step = 0.01

## Initial conditions
v_0 = 0.34
o_0 = 0.20
l_0 = 0.92

## Number of generations
gmax = 26

E = Environment(f_0, s_0, beta_v, beta_o, alpha, eps, rho, sigma_v, sigma_o, sigma_i, eta_f, eta_s, theta, gamma, P_mut,
                mutation_step)

data_folder = 'results'

## Creating the ancestral population
G = initial_generation(v_0, o_0, l_0, 0, 0, N_0, E)

## Return to previous simulation
if os.path.exists(data_folder + '/G'):
    g0, G = open_last_generation(data_folder, E)
else:
    g0 = 0
    save_generation(G, 0, data_folder)

# list_lineage_k = []
list_mean_k = []
tic = time.perf_counter()
for gi in range(g0 + 1, gmax + 1):
    print(gi)
    G = next_generation(G, v_evolve=False, o_evolve=False, l_evolve=False)
    if gi % 10 == 0:
        save_generation(G, gi, data_folder)
    if gi % 1 == 0:
        toc = time.perf_counter()
        print('##', 'Generation:', gi, '##')
        print(f"get 1 iterations in {toc - tic:0.4f} seconds")
        print('##   ##')
        tic = time.perf_counter()
    list_mean_k.append(np.mean([i.k for i in G]))

save_data_for_mathematica(data_folder, ngmin=0, ngmax=None)
with open(data_folder + "/Mathematica/meank.json", 'w') as file:
    json.dump(list_mean_k, file)
