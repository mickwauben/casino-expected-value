[README.md](https://github.com/user-attachments/files/34939368/README.md)

# Casino expected value analysis

Expected value (EV) and Monte Carlo analysis of a school casino project (roulette, slot machine, blackjack).

## Introduction

During high school for the subject computer science we had a final assignment to implement all the learning goals of the subject in a self made game. The subjects were i.a. CSV, Tkinter, loops and functions. It was a project in a group of two where my partner and I chose to make a simplified casino containing 3 games: blackjack, slot machine and roulette.

Now I've started my studies in econometrics I thought it would be interesting to investigate the probabilities and expected values on how these gambling games actually work. That's why I used the school project as a basis and constructed simulations to calculate the expected values on the long run. After these calculations I came across a mistake in the old school project: a slot machine where the casino loses on the long run. After some calculations with implementing a new RTP such that the casino wins I corrected the mistake.

Further in this document you can read my way of thinking, drafts and calculations to determine the expected values and correct the mistake. Do note that these calculations are based on simplified casino games (for blackjack) and that there's a small sampling error for every EV on the long run, so these numbers are not exact.

Note that every simulation is based on 1,000,000 rounds.

## Summary of results

EV = expected profit per €1 bet (negative = the casino wins on average).

| Game | Exact EV | Simulated EV |
|---|---|---|
| Roulette: red | -0.027 | -0.0275 |
| Roulette: black | -0.027 | -0.0264 |
| Roulette: green | -0.027 | -0.0293 |
| Roulette: even | -0.027 | -0.0271 |
| Roulette: odd | -0.027 | -0.0268 |
| Roulette: single number | -0.027 | -0.0267 |
| Slot machine (original payouts) | +0.0123 (casino loses) | not simulated |
| Slot machine (corrected payouts) | -0.0864 | -0.0898 |
| Blackjack (best fixed threshold, 16) | no exact value | -0.0738 |

Expected value = chance * profit + chance * loss

## Roulette

```
Red:    (+1)(18/37)  + (-1)(19/37) = -0.027
Black:  (+1)(18/37)  + (-1)(19/37) = -0.027
Green:  (+35)(1/37)  + (-1)(36/37) = -0.027
Odd:    (+1)(18/37)  + (-1)(19/37) = -0.027
Even:   (+1)(18/37)  + (-1)(19/37) = -0.027
Number: (+35)(1/37)  + (-1)(36/37) = -0.027
```

These are some basic drafts of the EV of each decision in the roulette game. Running the simulation we get the following results and see that they are (on average) correct with our expectations. Note that the sampling error for green and numbers are larger as the chance of winning is way less, but the win itself is way bigger.

```
red:    -0.027512
black:  -0.026414
green:  -0.029332
even:   -0.027118
odd:    -0.026808
number: -0.02674
```

## Slot machine

```
3 equal signs: 9/9 * 1/9 * 1/9   = 1/81
2 equal signs: 3 * (9/9 * 8/9 * 1/9) = 24/81
0 equal signs: 9/9 * 8/9 * 7/9   = 56/81

RTP = (A + 24B + 0C) / 81
```

RTP = (chance of 3 equal signs * payout A + chance of 2 equal signs * payout B + chance of 0 equal signs * payout C), where C is obviously 0 as you lose.

**Mistake in the old project.** Old values A = 10, B = 3:

```
RTP = (10)(1/81) + (3)(24/81) + (0)(56/81) = 82/81 > 1
```

The casino loses money on the long run, so we need a lower RTP.

**New payouts.** Standard RTP is between 85-98%, so let's take 92%:

```
(A + 24B) / 81 = 92/100  ->  A + 24B = 74.52  ->  A = 74.52 - 24B

B = 3  ->  A = 2.52   impossible, A must be larger than B
B = 2  ->  A = 26.52  ->  choose A = 26
```

Now RTP = (26 + 48)/81 = 91.36%, so EV = RTP - 1 = -0.0864.

Running the simulation we get -0.089838 as EV. Keeping in mind the sampling error we can conclude that these drafts are correct (on average).

## Blackjack

Note: This is a simplified version without splitting, shuffling, more decks etc. In the simulation the player ignores the dealer's visible card so we don't implement decision theory, although this could be a next step. Therefore, the house edge is on average higher (about 7%) than the standard real blackjack house edge (about 0.5%).

The dealer always stops at 17 (basic casino rules), so it is interesting to analyse if the casino still wins on average when the player uses the best fixed stopping threshold. Therefore we investigate every value from 12-20 where the player stops hitting. While running the simulation we get the following results (these EV values are average, not specific, keeping the sampling error in mind). We can conclude that the casino still wins in the long run for every fixed stopping threshold, and that the best stopping threshold for the player is 16.

| Player stops at | EV |
|---|---|
| 12 | -0.106406 |
| 13 | -0.093611 |
| 14 | -0.084327 |
| 15 | -0.076107 |
| 16 | -0.073764 |
| 17 | -0.079599 |
| 18 | -0.110604 |
| 19 | -0.201624 |
| 20 | -0.352509 |

![Blackjack: EV by stopping threshold](python%20Casino/blackjack_threshold.png)

## Files

- `python Casino/casino Informatica eindwerk.py`: the original school project (Tkinter, written in Dutch), with `roulette.csv` and `kaarten.csv`
- `python Casino/roulette_simulation.py`, `Slot_simulation.py`, `blackjack_simulation(...)`: the simulations used for the results above
- `Python Casino report`: the full write-up

The original school project was written in Dutch (variable names and comments); the analysis is in English.
