import numpy as np
import matplotlib.pyplot as plt
import random

#Test slučajnosti- plottamo gen brj u ovisnosti o redu pozivanja N

N, br = [], []
for i in range(20000):
    N.append(i) #ovo je broj poziva
    br.append(random.random()) #ovo je generirani broj


plt.figure(figsize = (12, 6))
plt.scatter(N, br, s = 1, c = "green")
plt.xlabel("Broj pozivanja")
plt.ylabel("Generirani broj")
plt.show()

#analiz grešku procjene M(k=3)
sum_k = 0
N_br  = 10**7 #br gen točaka
k  = 3
T = 10**3 #Period- svako koliko točaka računamo tražene vrij

N1, x_list, e_list = [], [], []

for i in range(1, N_br):
    x_i = random.random()
    sum_k += x_i**k
    if i % T == 0: #Ako je djeljivo tj period T
        x_k = sum_k / i #Trenutni moment
        e = np.abs(x_k - (1/(1+k)))
        x_list.append(x_k)
        e_list.append(np.sqrt(i)*e)
        N1.append(i)


plt.scatter(N1, e_list, s = 1, c = "blue")
plt.xlabel(r'N')
plt.ylabel(r'$\sqrt{N}$ $\epsilon$')
plt.show()