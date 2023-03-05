'''
Implements evaluation function for holding cards
'''


def leduc_eval(hold_card, community_card):
    '''
    Returns the strength of hold card or combination of hold card and
    community card
    '''

    cards = [hold_card.rank()] + [cc.rank() for cc in community_card]

    # If hold card and community card make a double
    # Use weight of 15 for double
    if cards.count(hold_card.rank()) > 1:
        return 15*14 + hold_card.rank()

    # Else use the weight as the rank of maximum of hold card and community card
    # The summation portion represents another card
    return 14 * max(cards) + min(cards)
