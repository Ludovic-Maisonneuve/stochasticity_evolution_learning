import time

from functions.dynamics import *
from functions.save_and_open import *

## Parameters' value

f_0, s_0 = 5, 1
beta_v, beta_o, alpha = 1.4, 1.3, 0.1
eps, rho = 0.05, 0.05
sigma_v = 0
sigma_o = 0
sigma_i = 0
eta_f, eta_s = 25, 5
theta = 0.1
gamma = 0.01

N_0 = 100
P_mut = 0.01
mutation_step = 0.01

## Initial conditions
v_0 = 0.13404
o_0 = 0.0762715
l_0 = 0.876229

## Number of generations
gmax = 500000

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

tic = time.perf_counter()
for gi in range(g0 + 1, gmax + 1):
    G = next_generation(G, v_evolve=True, o_evolve=True)
    if gi % 10 == 0:
        save_generation(G, gi, data_folder)
    if gi % 1000 == 0:
        toc = time.perf_counter()
        print('##', 'Generation:', gi, '##')
        print(f"get 1000 iterations in {toc - tic:0.4f} seconds")
        print('##   ##')
        tic = time.perf_counter()
