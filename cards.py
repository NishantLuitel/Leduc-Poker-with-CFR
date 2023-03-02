class Card():

    '''This class represents all cards in the deck'''

    '''Available card and suits for standard deck'''

    cards = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    suits = ['hearts', 'clubs', 'spade', 'diamond']

    @classmethod
    def total_cards(cls):
        '''
        Returns : total number of unique cards with this class
        '''

        return len(cls.cards)**len(cls.suits)

    def __init__(self, card, suit):
        '''
        Initialize card number and suit
        '''

        assert card in self.cards, "Only cards from A,2,3...K"
        assert suit in self.suits, "Only 4 suits available('hearts','clubs','spade','diamond')"

        self._card = card
        self._suit = suit

    def rank(self):

        return (self.cards.index(self._card) + 2)

    def __str__(self):

        return '({0},{1})'.format(self._card, self._suit)

    def __eq__(self, other):
        '''
        Implementing '==' operator
        '''

        return (self._card == other._card) and (self._suit == other._suit)

    def __lt__(self, other):
        '''
        Implementing '<' operator
        '''

        return (self.rank() < other.rank())

    @property
    def value(self):
        '''
        Returns the card as a tuple
        '''

        return (self._card, self._suit)
