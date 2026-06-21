"""Pruebas del verificador estático de Dynare.

Cubren un modelo RBC válido y una batería de modelos con errores típicos.
Ejecutar:  python -m pytest tests/ -q   (o)   python tests/test_verifier.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dynare_translate.core.verifier import analyze  # noqa: E402


# --------------------------------------------------------------------------- #
# Modelo RBC válido de referencia (8 variables, 8 ecuaciones)
# --------------------------------------------------------------------------- #
VALID_RBC = r"""
var Y C I K L W R A;
varexo e_a;
parameters beta alpha delta sigma phi rho_a;

beta  = 0.99;
alpha = 0.33;
delta = 0.025;
sigma = 1.0;
phi   = 1.0;
rho_a = 0.95;

model;
// Euler del consumo
C^(-sigma) = beta * C(+1)^(-sigma) * R(+1);
// Condicion trabajo-ocio
W = phi * L / C^(-sigma);
// Retorno del capital
R = alpha * A * K(-1)^(alpha-1) * L^(1-alpha) + (1-delta);
// Salario real
W = (1-alpha) * A * K(-1)^alpha * L^(-alpha);
// Funcion de produccion
Y = A * K(-1)^alpha * L^(1-alpha);
// Restriccion de recursos
Y = C + I;
// Acumulacion de capital
K = (1-delta) * K(-1) + I;
// AR(1) de la TFP
log(A) = rho_a * log(A(-1)) + e_a;
end;

shocks;
var e_a; stderr 0.01;
end;

stoch_simul(order=1, irf=40) Y C I K L W R;
"""


def test_valid_rbc_passes():
    r = analyze(VALID_RBC)
    assert r.ok, f"Esperaba sin errores, pero hubo: {r.errors}"
    assert r.stats["n_endogenous"] == 8
    assert r.stats["n_equations"] == 8
    assert r.stats["n_exogenous"] == 1
    assert r.stats["n_parameters"] == 6


def test_varexo_not_counted_as_endogenous():
    r = analyze(VALID_RBC)
    # e_a es varexo, no debe contarse como endogena
    assert r.stats["n_endogenous"] == 8


def test_bk_classification():
    r = analyze(VALID_RBC)
    # K y A aparecen con (-1) => estados ; C aparece con (+1) => jump
    assert r.stats["n_states"] >= 2
    assert r.stats["n_jumps"] >= 1


def test_equation_count_mismatch():
    # Quitamos la ecuacion de recursos (Y = C + I): 7 ecuaciones, 8 variables
    broken = VALID_RBC.replace("Y = C + I;", "")
    r = analyze(broken)
    assert not r.ok
    assert any("no coincide" in e for e in r.errors)


def test_undeclared_symbol():
    # Introducimos Z (no declarada) en la funcion de produccion
    broken = VALID_RBC.replace(
        "Y = A * K(-1)^alpha * L^(1-alpha);",
        "Y = Z * A * K(-1)^alpha * L^(1-alpha);",
    )
    r = analyze(broken)
    assert not r.ok
    assert any("no declarados" in e and "Z" in e for e in r.errors)


def test_missing_parameter_value():
    # Declaramos un parametro extra 'gamma' sin asignarle valor
    broken = VALID_RBC.replace(
        "parameters beta alpha delta sigma phi rho_a;",
        "parameters beta alpha delta sigma phi rho_a gamma;",
    )
    r = analyze(broken)
    assert any("sin valor asignado" in e and "gamma" in e for e in r.errors)


def test_unused_variable():
    # Declaramos Q en var pero nunca la usamos
    broken = VALID_RBC.replace(
        "var Y C I K L W R A;",
        "var Y C I K L W R A Q;",
    )
    r = analyze(broken)
    assert any("no aparecen en ninguna" in e and "Q" in e for e in r.errors)


def test_no_model_block():
    r = analyze("var Y C; varexo e; parameters beta; beta = 0.99;")
    assert not r.ok
    assert any("model" in e for e in r.errors)


def test_comments_are_stripped():
    model = r"""
    var x y;
    varexo e;
    parameters rho;
    rho = 0.9;
    model;
    /* ecuacion 1 */ x = rho * x(-1) + e;  // ley de movimiento
    y = x;  % identidad
    end;
    """
    r = analyze(model)
    assert r.ok, r.errors
    assert r.stats["n_equations"] == 2


def test_model_local_variable_not_counted():
    model = r"""
    var x y;
    varexo e;
    parameters rho;
    rho = 0.9;
    model;
    #aux = rho * x(-1);
    x = aux + e;
    y = x;
    end;
    """
    r = analyze(model)
    assert r.ok, r.errors
    # #aux no cuenta como ecuacion: deben quedar 2
    assert r.stats["n_equations"] == 2


def test_duplicate_declaration():
    model = r"""
    var x x y;
    varexo e;
    parameters rho;
    rho = 0.9;
    model;
    x = rho*x(-1) + e;
    y = x;
    end;
    """
    r = analyze(model)
    assert any("duplicada" in e for e in r.errors)


if __name__ == "__main__":
    # Runner mínimo sin pytest
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    passed = 0
    for fn in fns:
        try:
            fn()
            print(f"PASS  {fn.__name__}")
            passed += 1
        except AssertionError as exc:
            print(f"FAIL  {fn.__name__}: {exc}")
        except Exception as exc:  # noqa: BLE001
            print(f"ERROR {fn.__name__}: {exc}")
    print(f"\n{passed}/{len(fns)} pruebas OK")
    sys.exit(0 if passed == len(fns) else 1)
