import numpy as np
import matplotlib.pyplot as plt
from numba import njit

L = 32 #Neka fiksna veličina rešetke
c_values = np.linspace(0.10, 0.30, 25)
n_simulations = 300 #Manje jer mi nije toliko bitno 
#Gustoće raspodjele čvorova po radu
rho_values = [1.0, 0.9, 0.7]

EMPTY = -1 #Nova vrijednost za stanje koje je blokirano
SUSCEPTIBLE = 0
INFECTED = 1
RECOVERED = 2


@njit
def infected_neighbors(lattice, x, y, L):

    count = 0

    if lattice[(x+1)%L, y] == INFECTED:
        count += 1

    if lattice[(x-1+L)%L, y] == INFECTED:
        count += 1

    if lattice[x, (y+1)%L] == INFECTED:
        count += 1

    if lattice[x, (y-1+L)%L] == INFECTED:
        count += 1

    return count


@njit
def initialize_lattice(L, rho):

    lattice = np.zeros((L, L), dtype=np.int8)

    for x in range(L):
        for y in range(L):

            #Site nije blokiran
            if np.random.random() > rho:
                lattice[x, y] = EMPTY

            else:
                lattice[x, y] = SUSCEPTIBLE

    return lattice

@njit
def run_sir_diluted(L, c, rho):

    b = 1.0 - c

    lattice = initialize_lattice(L, rho)

    center = L // 2

    #Sada je potrebno osigurati da radimo na aktivnom čvoru
    while lattice[center, center] == EMPTY:

        center += 1

        if center >= L:
            center = L // 2
            break

    lattice[center, center] = INFECTED

    N = L * L

    touched_boundary = 0

    infected_exists = True

    while infected_exists:

        infected_exists = False

        for _ in range(N):

            x = np.random.randint(L)
            y = np.random.randint(L)

            state = lattice[x, y]

            if state == SUSCEPTIBLE:

                n_inf = infected_neighbors(lattice, x, y, L)

                p_inf = b * (n_inf / 4.0)

                if np.random.random() < p_inf:

                    lattice[x, y] = INFECTED

                    if (
                        x == 0 or
                        y == 0 or
                        x == L-1 or
                        y == L-1
                    ):
                        touched_boundary = 1

            elif state == INFECTED:

                infected_exists = True

                if np.random.random() < c:

                    lattice[x, y] = RECOVERED

    recovered = np.sum(lattice == RECOVERED)

    return recovered, touched_boundary


results = {}

for rho in rho_values:

    print(f"rho = {rho}")

    avg_sizes = np.zeros(len(c_values))

    second_moments = np.zeros(len(c_values))

    binder_ratios = np.zeros(len(c_values))

    percolation_probs = np.zeros(len(c_values))

    for ic, c in enumerate(c_values):

        cluster_sizes = np.zeros(n_simulations)

        percolating = 0

        for sim in range(n_simulations):

            size, touched = run_sir_diluted(L, c, rho)

            cluster_sizes[sim] = size

            percolating += touched

        S = np.mean(cluster_sizes)

        M = np.mean(cluster_sizes**2)

        U = M / (S**2)

        P = percolating / n_simulations

        avg_sizes[ic] = S

        second_moments[ic] = M

        binder_ratios[ic] = U

        percolation_probs[ic] = P

    results[rho] = {
        "S": avg_sizes,
        "M": second_moments,
        "U": binder_ratios,
        "P": percolation_probs
    }

plt.figure(figsize=(8,6))

for rho in rho_values:

    plt.plot(
        c_values,
        results[rho]["S"],
        marker='o',
        label=f'rho={rho}'
    )

plt.xlabel('c')
plt.ylabel('S = <N_R>')
plt.title('Prosječna veličina epidemije')
plt.legend()
plt.grid()
plt.show()


plt.figure(figsize=(8,6))

for rho in rho_values:

    plt.plot(
        c_values,
        results[rho]["P"],
        marker='o',
        label=f'rho={rho}'
    )

plt.xlabel('c')
plt.ylabel('P')
plt.title('Perkolacijska vjerojatnost')
plt.legend()
plt.grid()
plt.show()


plt.figure(figsize=(8,6))

for rho in rho_values:

    plt.plot(
        c_values,
        results[rho]["U"],
        marker='o',
        label=f'rho={rho}'
    )

plt.xlabel('c')
plt.ylabel('U = M / S²')
plt.title('Omjer uz efekt razrjeđivanja rešetke')
plt.legend()
plt.grid()
plt.show()