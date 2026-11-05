# Taller: el modelo RBC en Dynare, hueco por hueco

Material práctico del *crash course* de Dynare (Ventura & Echevarría). Es el mismo
modelo del handout y de la PD06 de Macro II, partes C y G: un RBC con trabajo
endógeno y calibración de King y Rebelo (1999).

El archivo de trabajo es `rbc_taller.mod`: tiene 20 huecos `???`, numerados
`[H1]`…`[H20]`, que completas en clase. La solución y el solucionario, con cada hueco
explicado, se comparten al final del taller.

## Antes de empezar

```matlab
>> addpath C:\dynare\7.1\matlab        % la ruta de tu instalación
>> cd <carpeta donde está rbc_taller.mod>
```

## Cómo se trabaja

El `.mod` está ordenado en los cinco bloques del handout (§3.2). Cada hueco trae en
su comentario una pista y la sección del handout que lo explica.

1. **Etapas 1 a 4 (H1–H18).** Escribe el preámbulo, las ocho ecuaciones, el estado
   estacionario y el choque. Dynare no corre mientras quede un `???` activo, así que
   estas cuatro etapas se completan antes de la primera corrida.
2. **Etapa 5 (H19–H20).** Avanza por los tres puntos de control. En cada uno corre
   `>> dynare rbc_taller` y compara con las cifras de abajo antes de seguir.

Mientras quede un `???` activo, Dynare se detiene antes de empezar, con un mensaje
como este (Dynare 7.1, al correr el archivo sin tocar):

```
ERROR: rbc_taller.mod: line 37, col 5: character unrecognized by lexer
Error using dynare (line 293)
Dynare: preprocessing failed
```

La línea y la columna señalan el primer hueco pendiente (aquí, `[H1]`). Si Dynare
se detiene en una línea sin `???`, lee el mensaje: el comando que falla dice dónde
buscar (handout, §3.13, "Depuración").

## Punto de control 1 — `steady` y `resid`

Dynare imprime el estado estacionario y los residuos de las ocho ecuaciones:

| y | c | i | k | h | r | w | a |
|---|---|---|---|---|---|---|---|
| 0.5673 | 0.4528 | 0.1145 | 4.5785 | 0.2000 | 0.0413 | 1.8919 | 1.0000 |

- Los ocho residuos deben salir en `0.000000`. Si uno no es cero, hay un error de
  álgebra en la Etapa 1 (H3–H7) o en la Etapa 3 (H16–H17). La ecuación con residuo
  es la sospechosa.
- Escribe `theta` en la ventana de comandos: debe dar `3.3424`.

## Punto de control 2 — `check` (H19)

- Módulos de los valores propios: `0.936`, `0.979`, `1.086` y uno gigantesco
  (≈ 10¹⁸, "infinito").
- Mensajes: `There are 2 eigenvalue(s) larger than 1 in modulus for 2
  forward-looking variable(s).` y `The order and rank conditions are verified.`
- Dos valores propios fuera del círculo unitario para dos *jumpers* (`c` y `r`).
  Ver handout, §3.6, Cuadro 3.5.

## Punto de control 3 — `stoch_simul` (H20)

En la regla de decisión (`POLICY AND TRANSITION FUNCTIONS`):

| | y | c | k | h |
|---|---|---|---|---|
| ante `k(-1)` | 0.0134 | 0.0524 | **0.9360** | −0.0147 |
| ante `eps` | 0.0060 | 0.0019 | 0.0041 | 0.0010 |

Y las IRF: en el impacto, el consumo sube 0.42 % y las horas 0.52 % sobre su
estado estacionario. Las horas cruzan a terreno negativo hacia el trimestre 30.

## Punto de control 4 — depreciación total (PD06, G.5)

```matlab
>> dynare rbc_taller -DDELTA1=1
```

- Estado estacionario: `r = 1.0163`, `k = 0.0375`, `c = 0.0770`; `theta` = `3.9683`.
- Valores propios: `0.333` (= 1 − α), `0.979`, `3.052` e infinito.
- Las horas no responden: su fila en la regla de decisión es nula y Dynare ni
  siquiera guarda `oo_.irfs.h_eps`.

## Para seguir

Con el taller completo, `graficar_irfs.m` (en `handout/`) dibuja las IRF con
estilo de publicación y `reconstruir_irf.m` las reconstruye a mano desde `oo_.dr`.
