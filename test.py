from cards import Card

from hand_eval import leduc_eval

from state import Player, State
# test cards.py
a = Card('A', 'spade')
m = Card('A', 'diamond')
b = Card('K', 'spade')

# print(a, a.value, a.cards, a.suits, Card.total_cards(), a < b, a == b, a > b, a.rank())
# print(isinstance(a, Card))

# test hand_eval.py
print("leduc_eval of {0} ,{0} is {1} ".format(a, leduc_eval(a, [m])))
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
state_dict = ss.start_state([a, b, b, a])


def bet_size_print(s):
    bs = []
    for p in s.players:
        bs.append(p.total)
    return bs


print(state_dict, 'Available actions: ', ss.actions())
print(ss.is_terminal())
succ_dict = ss.succesor_state('R', state_dict['turn'])
print(succ_dict, 'Available actions: ', ss.actions())
print(ss.is_terminal())
print(bet_size_print(ss))
succ_dict = ss.succesor_state('C', succ_dict['turn'])
print(succ_dict, 'Available actions: ', ss.actions())
print(ss.is_terminal())
print(bet_size_print(ss))
succ_dict = ss.succesor_state('R', succ_dict['turn'])
print(succ_dict, 'Available actions: ', ss.actions())
print(ss.is_terminal())
print(bet_size_print(ss))
succ_dict = ss.succesor_state('C', succ_dict['turn'])
print(succ_dict, 'Available actions: ', ss.actions())
print(ss.is_terminal())
print(bet_size_print(ss))
succ_dict = ss.succesor_state('R', succ_dict['turn'])
print(succ_dict, 'Available actions: ', ss.actions())
print(bet_size_print(ss))
print(ss.is_terminal())
print("pot total:", ss.pot_total(), "utility:", ss.utility())


print(ss.info_set(0))
print(ss.state)
