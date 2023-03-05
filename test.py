from cards import Card

from hand_eval import leduc_eval

from state import Player, State
# test cards.py
a = Card('A', 'spade')
b = Card('K', 'spade')

# print(a, a.value, a.cards, a.suits, Card.total_cards(), a < b, a == b, a > b, a.rank())
# print(isinstance(a, Card))

# test hand_eval.py
# print("leduc_eval of {0} ,{0} is {1} ".format(a, leduc_eval(a, [a])))
# print("leduc_eval of {0} ,{1} is {2} ".format(a, b, leduc_eval(a, [b])))
# print("leduc_eval of {0} ,{0} is {1} ".format(b, leduc_eval(b, [b])))


# test state.py
# test player class
# p = Player(0)
# print(p.has_raised)
# p.action('R')
# print(p.has_raised)

# test state class
ss = State(2, 2, leduc_eval)
state_dict = ss.start_state([a, b, b])
print(state_dict, 'Available actions: ', ss.actions())
print(ss.is_terminal())
succ_dict = ss.succesor_state('F', state_dict['turn'])
print(succ_dict, 'Available actions: ', ss.actions())
print(ss.is_terminal())
succ_dict = ss.succesor_state('R', succ_dict['turn'])
print(succ_dict, 'Available actions: ', ss.actions())
print(ss.is_terminal())
succ_dict = ss.succesor_state('R', succ_dict['turn'])
print(succ_dict, 'Available actions: ', ss.actions())
print(ss.is_terminal())
print(ss.info_set(0))
