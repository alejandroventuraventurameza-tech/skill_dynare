"""
Momentos del ciclo del RBC con trabajo (delta=0.025), filtrados con HP (lambda=1600),
para comparar con los hechos estilizados de EE.UU. (Galindo-Montecinos-Ortiz, Cap. 1,
Tabla 1.2). Reproduce el Cuadro 3.3 del handout.
"""
import numpy as np, scipy.sparse as sp
from scipy.sparse.linalg import spsolve

ss = dict(y=0.567292, c=0.452831, i=0.114462, k=4.578467, h=0.2, w=1.891919, a=1.0)
# Coeficientes de la regla de decision de Dynare (niveles): [k(-1), a(-1), eps]
pol = dict(
    y=(0.013385, 0.820454, 0.838053), c=(0.052384, 0.258377, 0.263919),
    i=(-0.038999, 0.562077, 0.574134), k=(0.936001, 0.562077, 0.574134),
    h=(-0.014734, 0.140109, 0.143114), w=(0.184015, 1.410839, 1.441102),
    a=(0.0, 0.979, 1.0))
sig, T, burn = 0.0072, 300000, 1000

def hp(x, lam=1600):
    n = len(x); I = sp.eye(n)
    D = sp.diags([1, -2, 1], [0, 1, 2], shape=(n-2, n))
    return x - spsolve((I + lam*(D.T@D)).tocsc(), x)

rng = np.random.default_rng(42)
eps = rng.normal(0, sig, T+burn); kprev = aprev = 0.0
S = {v: np.empty(T) for v in pol}
for t in range(T+burn):
    e = eps[t]; vals = {v: ck*kprev+ca*aprev+ce*e for v, (ck, ca, ce) in pol.items()}
    if t >= burn:
        for v in pol: S[v][t-burn] = vals[v]
    kprev, aprev = vals['k'], vals['a']

log = {v: S[v]/ss[v] for v in pol}
log['prod'] = log['y'] - log['h']          # productividad laboral y/h
cyc = {v: hp(log[v]) for v in log}
std = {v: np.std(cyc[v]) for v in log}

print(f"{'var':>6}{'std%':>8}{'rel.vol':>9}{'corr(y)':>9}{'ac1':>7}")
for v in ['y', 'c', 'i', 'k', 'h', 'w', 'prod', 'a']:
    rel = std[v]/std['y']
    cor = np.corrcoef(cyc[v], cyc['y'])[0, 1]
    ac1 = np.corrcoef(cyc[v][1:], cyc[v][:-1])[0, 1]
    print(f"{v:>6}{100*std[v]:8.2f}{rel:9.2f}{cor:9.2f}{ac1:7.2f}")
