# Leduc-Poker-with-CFR
Leduc poker is a 2 player simpified version of widely known Texas Hold'em poker with all of it's features

# Rules of Leduc poker

- Leduc is a simplified form of limit Texas hold’em poker, played with a deck of just 6 cards (two suits, three cards in each).
- Each player receives one private card and there is one shared community card.
- There are two rounds of betting, one before the community card is revealed and one after.
- In each round of betting, players have three options: fold, call, or raise.
- The maximum number of raises is capped at four per round.
- The player with the best hand (using a simplified poker hand ranking) at the end of the second round wins the pot.

# What is CFR?

- At the beginning of the algorithm, we initialize the counterfactual values of each information set to zero.
- The algorithm then plays many iterations of the game, where each iteration consists of the following steps:
  a. For each player, the algorithm traverses the game tree and computes the counterfactual values for each information set that the player can reach.
  b. Using the computed counterfactual values, the algorithm updates the regret values for each action that the player could have taken at each information set.
  c. The algorithm then computes a strategy for each player based on the current regret values.
  d. The algorithm uses the computed strategies to play a sample game and updates the counterfactual values of each information set.
- After many iterations, the algorithm converges to a Nash equilibrium, which is a pair of strategies that are optimal for both players

Credit : ChatGPT

# How to train?
Activate your virtual environment and install requirements

```{python}
pip install -r requirements.txt
```

Then, run cfr.py file
```{python}
python3 cfr.py
```

Play game in the console with:
```{python}
python3 play.py
```

Note : This repository implements must of it's functionality from 1st reference link

# References

- https://github.com/zanussbaum/pluribus
- https://github.com/IanSullivan/PokerCFR
- Steps to building a Poker AI by Thomas Trenner: https://medium.com/@thomas.trenner
- https://github.com/Jeremiah9000/Poker-with-Python
- Southey, F., et al. Bayes’ Bluff: Opponent Modelling in Poker.
- Lanctot, M. (2013). Monte Carlo Sampling and Regret Minimization for equilibrium computation and decision making in large extensive form games.

Note : Papers for the reference section are available in 'Literature' folder for this repository
