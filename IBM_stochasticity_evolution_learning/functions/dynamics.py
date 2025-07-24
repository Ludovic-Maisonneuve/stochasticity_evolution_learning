import random

from functions.classes import *


# Function to generate the next generation of individuals
def next_generation(G, v_evolve=True, o_evolve=True, l_evolve=True):
    # Extract parameters from the first individual's environment
    E = G[0].E
    P_mut, mutationstep = E.P_mut, E.mutation_step

    # Calculate the expected number of offspring
    k_mean = np.mean([i.k for i in G])
    list_fe = [i.get_fecundity() for i in G]
    expected_offspring_number = sum(list_fe)

    # Sample the number of offspring from a Poisson distribution
    N_o = np.random.poisson(expected_offspring_number)

    # Calculate probabilities of selecting individuals for reproduction
    sum_fe = np.sum(list_fe)
    p_fe = [fe / sum_fe for fe in list_fe]

    # Select individuals for reproduction according to their fecundity
    G_reprod = list(np.random.choice(G, N_o, p=p_fe))

    # Number of mutations expected in the offspring population
    N_mut = np.random.binomial(N_o, P_mut)

    # Generate offspring
    G_offspring = []
    for ni, ind in enumerate(G_reprod):
        if ni <= N_mut:  # If within the mutation quota
            # Mutate traits if within mutation probability
            if v_evolve:  # Mutate v if it evolves
                v_mut = np.clip(random.gauss(ind.v, mutationstep), 0, 1)
            else:
                v_mut = ind.v
            if o_evolve:  # Mutate o if it evolves
                o_mut = np.clip(random.gauss(ind.o, mutationstep), 0, 1)
            else:
                o_mut = ind.o
            if l_evolve:  # Mutate o if it evolves
                l_mut = np.clip(random.gauss(ind.l, mutationstep), 0, 1)
            else:
                l_mut = ind.l

            # Ensure the sum of l and v traits stay in the phenotypic space
            if v_mut + o_mut > 1:
                v_mut, o_mut = v_mut / (v_mut + o_mut), o_mut / (v_mut + o_mut)
            v_offspring, o_offspring, l_offspring = v_mut, o_mut, l_mut

        else:
            # No mutation; retain parent traits
            v_offspring, o_offspring, l_offspring = ind.v, ind.o, ind.l

        # Randomly select an oblique learning exemplar’s knowledge from the parental generation
        k_values = [ind.k for ind in G]
        k_o = np.random.choice(k_values)

        # Create an offspring individual with the potentially mutated traits
        offspring = Individual(v_offspring, o_offspring, l_offspring, ind.k, k_o, N_o, E)
        G_offspring.append(offspring)

    # Select the surviving offspring
    G_surviving_offspring = []
    k_mean_o = np.mean([i.k for i in G_offspring])  # Mean knowledge in the offspring generation
    for ind in G_offspring:
        # Determine if the offspring survive
        PS = ind.get_survival(N_o)  # Calculate survival probability
        # if PS>1:
        #    print(PS)
        if np.random.random() < PS:  # Determine whether the offspring survives or not
            G_surviving_offspring.append(ind)

    # Update the population size for each surviving offspring
    N = len(G_surviving_offspring)
    for ind in G_surviving_offspring:
        ind.N = N

    # Return the next generation
    return G_surviving_offspring
