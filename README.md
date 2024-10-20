# Introduction

## $R$-module DH

We have an $R$-module $M$, with public $m_{pub}$, exchange $m_{A}:=\alpha m_{pub}$, $m_B:=\beta m_{pub}$ for random, secret, commuting $\alpha, \beta\in R$, and derive a shared key from $m_{sh}:=\alpha\beta m_{pub}=\beta\alpha m_{pub}$.  The shared secret $m_{sh}$ should be unpredictable from the triple $(m_{pub}, m_A, m_B)\in M^3$.  At a minimum, the action of the ring should be one-way in some sense.

We could restrict to the group of units in $R$, i.e. $\alpha, \beta\in R^{\times}$, and work with a "lossless" group action.

## Linear action on tensors

We choose to work over a specific ring $R$ and $R$-module $M$. described below.

Let $S$ be a finite ring, $d$, $n$, positive integers, and $R=M_n(S)^d$ the $d$-fold product of $n\times n$ matrices over $S$.  Let $M$ be the $R$-module $(S^n)^{\otimes d}$, the $d$-fold tensor product of the free $S$-module of rank $n$.  $R$ acts diagonally on $M$, say from the left:
$$
L=(L_1,\ldots, L_d)\in R, \quad L\cdot(e_{i_1}\otimes\cdots e_{i_d})=(L_1e_{i_1})\otimes\cdots\otimes(L_de_{i_d}),
$$
extended linearly, where $\{e_1,\ldots,e_n\}$ is a basis for $S^n$.  One could also let $n=n_i$ vary with the index $1\leq i\leq d$, but we fix $n$ for simplicity.

For concreteness and ease of sampling, we can take $S=\mathbb{Z}/2^{\kappa}\mathbb{Z}$ or $S=\mathbb{F}_{2^{\kappa}}$.  As noted earlier, we could restrict to an action of $G=GL_n(S)^d=R^{\times}$ at the cost of rejecting sampling for invertible endomorphisms.

# Cube Diffie-Hellman

Let $T\in M$ be a fixed public tensor.  Alice and Bob randomly choose $A, B\in R$ that commute.  Alice sends Bob $T_A=A\cdot T$ and Bob sends Alice $T_B=B\cdot T$.  Their shared key is derived from
$$
T_{AB}=T_{BA}=A\cdot T_B=B\cdot T_A.
$$
For instance, Alice could act on the first half of the coordinates and Bob act on the second half:
$$
T_A = (A_1,\ldots,A_{d/2},I_n,\ldots I_n)\cdot T, \quad T_B = (I_n,\ldots I_n,B_1,\ldots,B_{d/2},)\cdot T.
$$

The public tensor $T$ and secret $A$, $B$, can be pseudo-randomly derived from seed, e.g. SHAKE them out.

# Security and practicality

## Is the action easy to compute?

If $T\in M$ and $L\in R$, then to compute $T_L$, one has to go through all $n^d$ basis elements $e_{i_1}\otimes\cdots\otimes e_{i_d}$, apply the coordinate maps $L_je_{i_j}$, and simplify.  This grows exponentially in $d$, polynomially in $n$, and linearly in $\kappa$.  However, the linear algebra is highly parallelizable.

## Is the action hard to invert?

Problem:  Given $T$ and $L\cdot T= T_L$, find $L$.  When $d=2$, this is easy; just (pseudo)invert $T$.  For larger $d$, this problem hopefully becomes difficult, a version of the "tensor isomorphism problem."

## What leaks?

How much information does the triple $(T, T_A, T_B)$ leak, or, for static $T$, what does a sequence $(T, T_{A^{(i)}}, T_{B^{(i)}})_i$ leak?


## Parameters

Suppose we work with $|S|=2^{\kappa}$, e.g. $S=\mathbb{Z}/2^{\kappa}\mathbb{Z}$ or $\mathbb{F}_{2^{\kappa}}$, and that we want 128 bits from each of Alice and Bob for example minimal parameters, i.e. $128=\kappa n^2d/2$.  Example parameters include:

1. $n=2$, $d=4$, $\kappa=16$ (large $\kappa$),
2. $n=2$, $d=64$, $\kappa=1$ (large $d$),
3. $n=8$, $d=4$, $\kappa=1$ (large $n$).

The size of all exchanged data (say $T$, $T_A$, $T_B$) is $3\kappa n^d$.

# Prototype implementation

We provide prototype implementations for $S=\mathbb{Z}/(2^{\kappa})$.  Here's  an example run with the second parameter set above:

> $ python3 cube_dh.py  
> parameters : n = 2, d = 4, kappa = 16 
>
> T (public): 
> [[[[44224  7839] 
> [35456  9446]] 
> [[ 5691 27294] 
> [61054 21628]]] 
> [[[10104 55518] 
> [15792 13952]] 
> [[52366 25746] 
> [48668 58642]]]] 
>
> A (secret): 
> [[[18541 62731] 
> [59340  2209]] 
> [[18399  3182] 
> [53200 59952]]] 
>
> B (secret): 
> [[[51858 30665] 
> [10444 58045]] 
> [[51928 37156] 
> [64342 38030]]] 
>
> T_A (public): 
> [[[[ 9346 34466] 
> [38580 18704]] 
> [[29769 48476] 
> [56954  3762]]] 
> [[[45572 48496] 
> [46600 30468]] 
> [[18802 23930] 
> [55876  1666]]]] 
>
> T_B (public): 
> [[[[58204 65526] 
> [15320 65302]] 
> [[55956 16366] 
> [  458 45712]]] 
> [[[44056 45712] 
> [13584 16776]] 
> [[30544 60182] 
> [11260 49158]]]] 
>
> T_AB = T_BA (secret): 
> [[[[30704 31100] 
> [ 6300 36160]] 
> [[50164 47816] 
> [58422 44146]]] 
> [[[49584 17788] 
> [54888 11804]] 
> [[64960 61854] 
> [57524 57894]]]] 
>
> SUCCESS, key = e2dd6a754d1571e462425df88cc5cd89b3639cbffdcbb2d52522b48b47767848

# References
See [https://home.cs.colorado.edu/~jgrochow/pubs-by-topic.html](https://home.cs.colorado.edu/~jgrochow/pubs-by-topic.html) under "Tensors" for starting references exploring the computational complexity of tensor isomorphism and related problems.
