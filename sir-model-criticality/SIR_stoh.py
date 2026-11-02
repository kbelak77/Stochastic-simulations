import numpy as np
import matplotlib.pyplot as plt
from numba import njit

#Odabrane vrijednosti za veličine rešetki (broj čvorova)
L_values = [32, 64, 128]

#U intervalu vrijednosti oko poznate kritične (Ispitujemo ponašanje u kritičnoj zoni)
c_values = np.linspace(0.10, 0.30, 25) #Njihovo od 0.15 do 0.2

n_simulations = 1000 #Broj neovisnih MC realiz epidemije (za set parametara)

#Stanjima pripisane vrijednosti da bi mogli mapirat/spremit
SUSCEPTIBLE = 0
INFECTED = 1
RECOVERED = 2

#Fja provjera kroz petlju koliko je inficiranih susjeda (bitno za vjerojatnost inficiranja)
@njit
def infected_neighbors(lattice, x, y, L):

    count = 0

    #Gore
    if lattice[(x - 1 + L) % L, y] == INFECTED:
        count += 1

    #Dolje
    if lattice[(x + 1) % L, y] == INFECTED:
        count += 1

    #Lijevo
    if lattice[x, (y - 1 + L) % L] == INFECTED:
        count += 1

    #Desno
    if lattice[x, (y + 1) % L] == INFECTED:
        count += 1

    return count


#Fja jedna realizacija MC simulacije epidemije
@njit
def run_sir(L, c):

    b = 1.0 - c

    lattice = np.zeros((L, L), dtype=np.int8)

    center = L // 2

    lattice[center, center] = INFECTED

    touched_boundary = 0

    N = L*L

    infected_exists = True

    while infected_exists:

        infected_exists = False

        #Jedan Monte Carlo sweep
        for _ in range(N):

            #Slučajni čvor
            x = np.random.randint(L)
            y = np.random.randint(L)

            state = lattice[x, y]

            #Zaraza
            if state == SUSCEPTIBLE:

                n_inf = infected_neighbors(lattice, x, y, L)

                infection_probability = b * (n_inf / 4.0) #Vjerojatnost ovisi o udjelu zaraženih susjeda (od 4)

                if np.random.random() < infection_probability:

                    lattice[x, y] = INFECTED

                    if x == 0 or y == 0 or x == L-1 or y == L-1:
                        touched_boundary = 1
            #Oporavak
            elif state == INFECTED:

                infected_exists = True

                if np.random.random() < c:

                    lattice[x, y] = RECOVERED

    recovered = np.sum(lattice == RECOVERED)

    return recovered, touched_boundary

#Monte Carlo
results = {}

for L in L_values:

    print(f"Simuliranje L = {L}")

    avg_sizes = np.zeros(len(c_values))
    second_moments = np.zeros(len(c_values))
    binder_ratios = np.zeros(len(c_values))
    percolation_probs = np.zeros(len(c_values))
    UP = np.zeros(len(c_values))

    for ic, c in enumerate(c_values):

        cluster_sizes = np.zeros(n_simulations)

        percolating = 0

        for sim in range(n_simulations):

            #Runnanje funkcije
            size, touched = run_sir(L, c)

            cluster_sizes[sim] = size
            #Parametar touched opisuje u koliko iteracija je dotaknuta stranica kod klastera (nastao tzv beskonačni klaster)
            percolating += touched

        #Relevantne veličine za evaluaciju modela...
        S = np.mean(cluster_sizes)

        M = np.mean(cluster_sizes**2)

        U = M / (S**2)

        #Order parametar definiran da odgovara perkolacijskom usporedbe radi
        P = percolating / n_simulations

        #Specifičan c
        avg_sizes[ic] = S
        second_moments[ic] = M
        binder_ratios[ic] = U
        percolation_probs[ic] = P
        UP[ic] = U*P

    #Indeksirano ovisno o specif veličini rešetke L
    results[L] = {
        'S': avg_sizes,
        'M': second_moments,
        'U': binder_ratios,
        'P': percolation_probs,
        'UP': UP
    }

#Srednja vrijednost broja oporavljenih S u ovisnosti o c
plt.figure(figsize=(8,6))

for L in L_values:
    plt.plot(c_values, results[L]['S'],
             marker='o', label=f'L={L}')

plt.xlabel('c')
plt.ylabel(r'S = $<N_R>$')
plt.title('Srednji broj oporavljenih čvorova')
plt.legend()
plt.grid()
plt.show()

#Perkolacijska vjerojatnost P u ovisnosti o c
plt.figure(figsize=(8,6))

for L in L_values:
    plt.plot(c_values, results[L]['P'],
             marker='o', label=f'L={L}')

plt.xlabel('c')
plt.ylabel('P')
plt.title('Perkolacijska vjerojatnost P')
plt.legend()
plt.grid()
plt.show()

#Ponašanje omjera u ovisnosti o c

plt.figure(figsize=(8,6))

for L in L_values:
    plt.plot(c_values, results[L]['U'],
             marker='o', label=f'L={L}')

plt.xlabel('c')
plt.ylabel('U = M/S²')
plt.title(r'Omjer U')
plt.legend()
plt.grid()
plt.show()

#Ponašanje omjera u ovisnosti o c

plt.figure(figsize=(8,6))

for L in L_values:
    plt.plot(c_values, results[L]['UP'],
             marker='o', label=f'L={L}')

plt.xlabel('c')
plt.ylabel('UP')
plt.title(r'Ponašanje umnoška UP u ovisnosti o c')
plt.legend()
plt.grid()
plt.show()