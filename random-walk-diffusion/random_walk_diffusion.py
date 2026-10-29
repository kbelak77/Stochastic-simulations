import numpy as np
import matplotlib.pyplot as plt
import random
from scipy.optimize import curve_fit
import time

N_setaca = 64000
N = 200 #vremenski koraci
min, max = -3, 3
js = [t for t in range(30, 201, 30)] #do 200s neki  kdt
js.append(199)
pozicije = np.zeros(N_setaca)

#funkcija srednjeg pomaka kv kroz vrijeme/korake
x2_t = []
raspodjele = {}

for i in range(1,N):
    for j in range(N_setaca): #po broju šetača
        #pomak = random.randint(min,max) 
        random_br = random.random()
        pomak = random_br * 6 - 3 #promjena intervala/skaliranje
        pozicije[j]+= pomak #pomak j-tog setaca
    x2 = (1/N_setaca)*sum(pozicije ** 2) #za neki t odnosno korak rač sr vrij
    x2_t.append(x2)#pohrna srednjih vrijednosti pomaka šetača za jedan korak
    if i in js:
        raspodjele[i] = pozicije.copy() #za specifična vremena i-ti član liste raspodjele sadrži pozicije šetača

koraci = [Ni for Ni in range(1,N)]

def f(D,t):
    return 2.0*D*t

plt.figure(figsize=[6, 4])
plt.plot(koraci, x2_t, color = 'hotpink', lw = 2.5, label = 'srednja vrijednost kvadrata položaja šetača') #ovisnost srednje vrijednosti kvadrata položaja o vremenu

a, _ = curve_fit(f, koraci, x2_t)
D_fit = a[0]

plt.title(r"Ovisnost $\langle x^{2} \rangle$(t) o vremenskom koraku")
plt.xlabel("t [s]")
plt.ylabel(r"$\langle x^{2}\rangle$ (t) [cm$^2$]")
plt.plot(koraci, f(np.array(koraci), D_fit), label= f'fit na funkciju (D = {round(D_fit, 3)})', color = 'blue', lw = 1.0)
plt.legend(loc = 'upper left')
plt.savefig("x2_t.png")
plt.show()
time.sleep(1)

#####DRUGI DIO#####

dx = 1.0
dt = 0.1
x_min = -100
x_max = 100
x_evi = np.arange(x_min, x_max + dx, dx) #radi diskretizaciju
x_centri = (x_evi[:-1] + x_evi[1:]) / 2 #zbog razdiobi

L=200
T= 200
b= 1.5
Nx = int(L/dx)
Nt = int(T/dt)

alpha = b * (dt/(dx**2))
if alpha >(1/2):
    print('Rješenje nije stabilno za ovaj odabir dx.')

x = np.linspace(-100, 100 , Nx) 
t = np.linspace(0, T, Nt) 
fja = np.zeros((Nt, Nx))

fja[0, Nx//2] = 1.0/dx #indeksi, ne koordinatne vrijednosti!! diskretizacija položaja/vremena

#EKSPLICITNA
for j in range(0, Nt-1):
    for i in range(1, Nx-1): 
        fja[j+1, i] = alpha*fja[j, i+1] + (1-2*alpha)*fja[j, i] + alpha*fja[j, i-1]

    fja[j+1, 0] = 0
    fja[j+1,-1] = 0


#pozicije sadrži sve pozicije svih šetača

def razdioba(pozicije, x_evi, dx):
    broj_č = np.zeros(len(x_evi) - 1)

    for x in pozicije:
        if x_min <= x < x_max:
            indeks = int((x - x_min) // dx)
            broj_č[indeks] += 1 #u tom se odjeljku našao

    #normaliz
    P = broj_č / (len(pozicije) * dx)
    return x_centri, P

alphas = [0.2, 0.3,  0.4, 0.6, 0.7, 0.8, 1.0]
plt.figure(figsize=(8,5))

for k in range(len(js)):
    pozicije_t = raspodjele[js[k]]
    x_val, P_x = razdioba(pozicije_t, x_evi, dx)
    plt.plot(x_val, P_x, color='hotpink', alpha=alphas[k], label = f't ={js[k]} s')


plt.xlabel('x [cm]')
plt.ylabel(r'$P(x) / (N dx)$ [cm $^{-1}$]')
plt.title(f'Funkcija razdiobe šetača u prostoru za određena vremena t')
plt.grid(True)
plt.legend()
plt.savefig("P(x)_graf.png")
plt.show()
time.sleep(1)


plt.figure(figsize=(8,5))
alphas = [0.2, 0.3,  0.4, 0.6, 0.7, 0.8, 1.0]
for k in range(len(js)):
    pozicije_t = raspodjele[js[k]]
    x_val, P_x = razdioba(pozicije_t, x_evi, dx)
    plt.plot(x_val, P_x, color='hotpink', alpha=alphas[k], label = f't={js[k]} s')
    plt.plot(x, fja[int(js[k]/dt)], label=f"Eksplicitna t={js[k]}s", color = 'red', lw = 1.0)

plt.xlabel('x [cm]')
plt.ylabel(r'$P(x) / (N dx)$ [cm $^{-1}$]')
plt.title('Usporedba funkcije razdiobe s rješenjem difuzijske jednadžbe eksplicitnom metodom.')
plt.grid(True)
plt.legend()
plt.savefig("P(x)_difuzija_graf.png")
plt.show()
time.sleep(1)