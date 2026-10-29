#Osmislite i provedite test za ran1 (ili ekvivalentni generator) na temelju računanja broja
#𝜋 = 3.14159 26535 89793 23846 26433 83279 50288 41971 69399 37510 ⋯.
#Priložite kod i graf

import numpy as np
import matplotlib.pyplot as plt
import random
#grafički prikaz točaka i odsječka kružnice
N1 = 10000
num1 = 0
X, Y = [], []
for i in range(1, N1):
    x_i1 = random.random()
    y_i1 = random.random()
    X.append(x_i1)
    Y.append(y_i1)

x = np.linspace(0, 1, N1)
y = np.sqrt(1 - x**2)
plt.scatter(X, Y, s = 0.1, c = "green")
plt.plot(x, y)
plt.title("Grafički prikaz generiranih točaka")
#plt.show()

#provjera generatora
N2  = 200000
T = 5*10**(2)
N_s, e_s, pi_s = [], [], []

num2 = 0 #brojač za površinu kruga

for j in range(1,N2):
    #generiranje nekih točaka u xy ravnini
    x_j2 = random.random()
    y_j2 = random.random()
    #ako se nalaze unutar jedinične kružnice podižem vrijednost brojača
    if x_j2**2 + y_j2**2 <=1:
        num2+=1
    if j%T==0: #računamo odstupanje za neke točke
        pi = 4*num2/j #vjerojatnost da je točka u kružnici ovom relacijom ovisi o površini (vj je num/i)
        pi_s.append(pi)
        #eps = np.abs(pi-np.pi)
        eps = pi-np.pi
        e_s.append(np.sqrt(j)*eps)
        N_s.append(j)


plt.figure(figsize = [12, 6])
plt.subplot(2, 1, 1)
plt.plot(N_s, pi_s, c = "blue")
plt.axhline(np.pi)
plt.xlabel(r'N')
#plt.xscale("log")
plt.ylabel(r'pi')
plt.title(r'Usporedba broja $\pi_{i}$ sa $\pi$')

plt.subplot(2, 1, 2)
plt.plot(N_s, e_s, c = "blue")
plt.axhline(0, linestyle = '--')
plt.xlabel(r'N')
#plt.xscale("log")
plt.ylabel(r'$\sqrt{N}$ $\epsilon$')
plt.title(r'Funkcijska ovisnost $\sqrt{N}$ $\epsilon$ o N')
plt.subplots_adjust(hspace = 0.43) #prilagodba prikaza
plt.show()

