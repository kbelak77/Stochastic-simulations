# Kritično ponašanje stohastičkog SIR modela na kvadratnoj rešetki

*Critical behaviour of the stochastic SIR model on a square lattice: Monte Carlo simulation, link to percolation theory and effect of lattice dilution (immunization). Paper and code comments in Croatian.*

Seminarski rad iz kolegija *Stohastičke simulacije u klasičnoj i kvantnoj fizici*, PMF Split, svibanj 2026. ([SIR_MODEL_CRITICALITY.pdf](SIR_MODEL_CRITICALITY.pdf))

Monte Carlo simulacija SIR (Susceptible–Infected–Recovered) epidemije na 2D kvadratnoj rešetki s periodičnim rubnim uvjetima, prema radu de Souze, Toméa i Ziffa. U okolini kritične točke c_c ≈ 0.1765 analiziraju se srednji broj oporavljenih čvorova S = ⟨N_R⟩, perkolacijska vjerojatnost P, omjer U = M/S² i umnožak U·P. Dodatno se proučava utjecaj razrjeđivanja rešetke (imunizacije) za gustoće ρ = 1.0, 0.9 i 0.7.

| Datoteka | Opis |
|---|---|
| `SIR_stoh.py` | Osnovni model: L = 32, 64, 128, 25 vrijednosti c ∈ [0.10, 0.30], 1000 realizacija po točki. Crta S, P, U i U·P. |
| `imunizacija.py` | Model s razrijeđenom rešetkom: L = 32, ρ = 1.0, 0.9, 0.7, 300 realizacija po točki. Crta S, P i U. |

## Pokretanje

```bash
pip install -r requirements.txt
python SIR_stoh.py
python imunizacija.py
```

Simulacije su ubrzane Numbinim JIT kompajlerom (`@njit`). Osnovni model s punim parametrima (posebno L = 128) traje dugo. Za brzu provjeru smanji `n_simulations` ili izbaci 128 iz `L_values`.
