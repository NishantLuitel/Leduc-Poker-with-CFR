import pickle
from state import State
from cards import Card
from hand_eval import leduc_eval
from itertools import permutations
import numpy as np

with open('trained_models/cfr_train2.pickle', 'rb') as f:
    node_map, action_map = pickle.load(f)


# print(node_map[0].keys())


num_players = 2
num_rounds = 2
num_cards = num_players+1


cards = [Card('J', 'spade'), Card('Q', 'spade'), Card('K', 'spade'),
         Card('J', 'diamond'), Card('Q', 'diamond'), Card('K', 'diamond')]

card_combinations = [list(t) for t in set(permutations(cards, num_cards))]
random_int = np.random.choice(len(card_combinations))

card = card_combinations[random_int]
ss = State(num_players, num_rounds, leduc_eval)
ss.start_state(card)

ai_id = int(input("Choose AI to play as player 0 or 1 by pressing '0' or '1':"))
ai_card = ss.get_player(ai_id).card
human_id = int(not ai_id)

print("Your card: {0}".format(ss.get_player(human_id).card))

v = 0
while(not ss.is_terminal()):
    turn = ss.state['turn']
    r = ss.state['round']
    if r == 1 and v == 0:
        v = 1
        print("Community card revealed:", ss.state['cc'])

    if turn == ai_id:
        info_set = ss.info_set(ai_id)
        node = node_map[turn][info_set]
        strategy = node.avg_strategy()
        random_action = np.random.choice(
            list(strategy.keys()), p=list(strategy.values()))
        print("Opponent action: ", random_action)
        ss.succesor_state(random_action)
    else:
        human_card = ss.get_player
        valid_actions = ss.actions()
        action = input("Choose action from '{0}':".format(valid_actions))
        ss.succesor_state(action)
else:
    print("AI card is {0}".format(ai_card))
    print("Your score: {0}".format(ss.utility()[human_id]))
