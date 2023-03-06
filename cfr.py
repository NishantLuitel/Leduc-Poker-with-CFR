from cards import Card
from itertools import permutations
from tqdm import tqdm
import numpy as np
from game_tree import Tree
import sys
import pickle

from state import State
from hand_eval import leduc_eval

sys.setrecursionlimit(6000)


def learn(num_iterations, cards, num_cards, gameT):
    '''
    Implements the learning algorithm
    '''

    card_combinations = [list(t) for t in set(permutations(cards, num_cards))]
    num_players = num_cards-1
    num_rounds = 2
    # gameT = Tree(num_players)

    for _ in tqdm(range(num_iterations), desc='learning'):

        # Select a random card combination
        random_int = np.random.choice(len(card_combinations))

        # Initialize start state
        ss = State(num_players, num_rounds, leduc_eval)
        ss.start_state(card_combinations[random_int])
        wts = np.ones(num_players)
        gameT.accumulate_regrets(ss, wts)

    with open('trained_models/cfr_train3.pickle', 'wb') as f:
        pickle.dump((gameT.node_map, gameT.action_map), f)
    print(gameT.node_map)


if __name__ == '__main__':
    num_players = 2
    num_iterations = 20000

    # number of cards is 3 because we include community card in it
    num_cards = num_players + 1
    cards = [Card('J', 'spade'), Card('Q', 'spade'), Card('K', 'spade'), Card(
        'J', 'diamond'), Card('Q', 'diamond'), Card('K', 'diamond')]

    game_tree = Tree(num_players)

    learn(num_iterations, cards, num_cards, gameT=game_tree)
