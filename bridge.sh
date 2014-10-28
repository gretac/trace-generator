#!/bin/bash
start=$(python ~/Documents/python/model/model.py)
evo=0
jump=0


echo "require(yuima)
grid = setSampling(Terminal = 1, n = 1000)
jump = list(intensity = \"0.5\", df = list(\"dnorm(z,0,1)\"))
m1 = setModel(drift = \"mu*X\", diffusion = \"sigma*X\", state.var = \"X\", solve.var = \"X\", xinit = $start, jump.coeff = \"$jump\", measure = jump, measure.type=\"CP\")
X = simulate(m1, true.param = list(mu = $evo, sigma = 0.01), sampling = grid)
plot(X)" > temp.r

R --save < temp.r
