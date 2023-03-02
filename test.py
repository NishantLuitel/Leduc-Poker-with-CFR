from cards import Card

a = Card('A', 'spade')
b = Card('2', 'spade')

print(a, a.value, a.cards, a.suits, Card.total_cards(), a < b, a == b, a > b, a.rank())
