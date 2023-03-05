from cards import Card
from itertools import permutations
from tqdm import tqdm
import numpy as np
from game_tree import Tree

from state import State
from hand_eval import leduc_eval


def learn(num_iterations, cards, num_cards):
    '''
    Implements the learning algorithm
    '''

    card_combinations = [list(t) for t in set(permutations(cards, num_cards))]
    num_players = num_cards-1
    num_rounds = 2

    for _ in tqdm(range(num_iterations), desc='learning'):

        # Select a random card combination
        random_int = np.random.choice(len(card_combinations))

        # Initialize start state
        ss = State(num_players, num_rounds, leduc_eval)
        state = ss.start_state(card_combinations[random_int])
        probs = np.ones(num_players)


if __name__ == 'main':
    num_players = 2
    num_iterations = 10000

    # number of cards is 3 because we include community card in it
    num_cards = num_players + 1
    cards = [Card('J', 'spade'), Card('Q', 'spade'), Card('K', 'spade'), Card(
        'J', 'diamond'), Card('Q', 'diamond'), Card('K', 'diamond')]

    game_tree = Tree(num_players)

    learn(10000, cards, num_cards)
