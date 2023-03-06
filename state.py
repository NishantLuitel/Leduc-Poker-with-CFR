'''
This module implements the Player , Action and State class required for
state implementation

'''

from cards import Card
from copy import deepcopy, copy
import numpy as np


class Player():

    def __init__(self, id):
        self._id = id
        self._bet_size = 1
        self.total = 1
        self._active = True
        self._raised = False

    def give_card(self, card):
        if isinstance(card, Card):
            self._card = card

    @property
    def card(self):
        return self._card

    @property
    def bet_size(self):
        return self._bet_size

    def __repr__(self):

        return 'Player({0})'.format(self._id)

    def _fold(self):
        '''
        Implementing action 'fold' by player
        '''

        # Make the player inactive if he folds
        self._active = False
        self._raised = False

    def _call(self, amount):
        '''
        Implementing action 'call' by player
        '''

        # Increase number of bets
        self._bet_size += amount
        self.total += amount

    def _bet(self, amount):
        '''
        Implementing action 'bet' by player
        '''

        # Increase number of bets
        self._bet_size += amount
        self.total += amount

    def _raise(self):
        '''
        Implementing action 'raise' by player
        '''

        # Set the 'raised' variable to True
        self._raised = True

    def _check(self):
        '''
        Implenting action 'check' by player
        '''
        pass

    def action(self, act: str, bet_amount=0):
        '''
        Take the action as given by 'act' variable
        '''

        if act == 'F':
            self._fold()
        elif act == 'R':
            self._raise()
            self._bet(bet_amount)
        elif act == 'C':
            self._call(bet_amount)
        elif act == 'Ch':
            self._check()
        # else:
        #     self._bet()

    @property
    def active(self):
        '''
        Return if the player is active(has folded)
        '''
        return self._active

    @property
    def has_raised(self):
        '''
        Return if the player is active(has folded)
        '''
        return self._raised

    @property
    def id(self):
        '''Returns player id'''

        return self._id

    def reset_bet(self, value=1):
        self._bet_size = value

    def reset_total(self):
        self.total = 1


class State():

    def __init__(self, num_players, num_rounds, hand_eval):
        '''
        Define the variables that initializes state
        '''

        self.num_rounds = num_rounds
        self.num_players = num_players
        self.eval = hand_eval
        self.players = [Player(id) for id in range(num_players)]
        self.history = [[] for _ in range(self.num_rounds)]

        # state as (players,community_card,turn,round)
        self._state = {}

    def __copy__(self):
        '''Implement copy function'''

        new_state = State(self.num_players, self.num_rounds, self.eval)

        new_state.players = deepcopy(self.players)
        new_state.history = deepcopy(self.history)
        new_state._state = deepcopy(self._state)

        return new_state

    def start_state(self, cards, turn=0, round_no=0):
        '''

        Define the start state for the game
        '''

        # Community card empty if
        community_card = ''
        if len(cards) > len(self.players):
            community_card = cards[-1]

        for card, p in zip(cards, self.players):
            p.give_card(card)

        turn = turn
        round_no = round_no
        self._state = {'players': self.players, 'cc': community_card,
                       'turn': turn, 'round': round_no,
                       'history': self.history, 'bet_size': 1}
        return self._state

    @property
    def state(self):

        return self._state

    def get_player(self, id, players=None):
        '''
        Returns player with given id if present
        '''
        if not players:
            players = self.players

        for p in players:
            if p._id == id:
                return p
        return None

    def num_active_players(self):
        '''Returns the number of players who are active(haven't folded)'''

        return sum([p.active for p in self.players])

    def info_set(self, id):
        '''
        Returns information set for the given player id
        '''
        player = self.players[id]
        r = self._state['round']

        # Only keep Community card in information set if round is > 0
        # Because community card is only revealed after 1st round
        info_set = f"{player.card}|{'' if r == 0 else self._state['cc']}|{self._state['history'][:r+1]}"
        return info_set

    def succesor_state(self, action, id=0, update=True, return_object=False):
        '''
        Returns the next state, given the action for a player
        '''

        if not update:
            new_state = copy(self)
        else:
            new_state = self

        active_players = new_state.num_active_players()

        r = new_state._state['round']
        turn = new_state._state['turn']

        if new_state.is_terminal():
            if return_object:
                return new_state
            return new_state._state

        # Take action
        player = new_state.get_player(turn)
        match_amount = new_state._state['bet_size'] - player.total
        # print("match_amount:", match_amount)
        current_bet_size = 2*(r+1)
        amount = 0
        if action == 'R':
            amount = current_bet_size + match_amount
        elif action == 'C':
            amount = match_amount
        player.action(action, amount)
        new_state._state['bet_size'] = player.total

        # Update History

        new_state._state['history'][r].append(action)

        # Find the turn
        while(True):
            turn = (turn+1) % self.num_players
            if new_state.players[turn].active:
                break

        # Update turn
        new_state._state['turn'] = turn

        # Update round
        if len(new_state._state['history'][r]) - \
                new_state._state['history'][r].count('Ch') == active_players:
            if new_state._state['round'] < self.num_rounds - 1:
                new_state._state['round'] += 1

            # Reset the raised variable for next round
            for p in new_state.players:
                p._raised = False
                p.reset_bet(1)
            # new_state._state['bet_size'] = 1

        # Return successor state
        if return_object:
            return new_state
        return (new_state._state)

    def actions(self):
        '''
        Returns available actions to take for current player
        Assumes: the terminal state hasn't been reached even if it is
        '''

        num_raises_so_far = sum([p.has_raised for p in self.players])
        round_no = self._state['round']
        history_for_round = self._state['history'][round_no]

        history = []
        for h in self._state['history']:
            history += h

        if num_raises_so_far == self.num_players:
            return ['F', 'C']
        else:
            if len(history_for_round) == 0 and round_no == 0:
                return ['F', 'R',  'Ch']
            elif (round_no == 0 and all(['Ch' == a or 'F' == a for a in history_for_round])
                  and history_for_round.count('Ch') < self.num_players):
                return ['F', 'R', 'Ch']
            else:
                active_players = self.num_active_players()
                if 'R' in history_for_round[-1:-(active_players):-1]:
                    return ['F', 'C', 'R']
                return ['F', 'R']

    def is_terminal(self):
        '''Determine if the current state is indeed terminal'''

        # Terminal if there is only one active player
        active_players = self.num_active_players()
        if active_players == 1:
            return True

        # Terminal if
        # if self._state['history'][r].count('F') == self.num_players-1:
        #     return True

        # Terminal if the game is in final round, and all the active players
        #  have had an action(disregarding 'Check' action)

        r = self._state['round']
        if self._state['round'] == self.num_rounds-1 and \
                len(self._state['history'][r]) - self._state['history'][r].count('Ch') == \
                active_players:
            return True

        return False

    def utility(self):
        '''
        Finds utility value for every player
        '''

        active_players = self.num_active_players()
        if active_players == 1:
            hand_scores = []
            winners = [p.id for p in self.players if p.active]

        else:
            # Get the community card if in round 1
            cc = '' if self._state['round'] == 0 else self._state['cc']
            hand_scores = [self.eval(p.card, [cc])
                           for p in self.players]
            active_hand_scores = [self.eval(p.card, [cc])
                                  for p in self.players if p.active]
            winners = []

            # Find maximum hand score for active players
            maximum = max(active_hand_scores)

            # Append all the players that have above maximum value
            for i, score in enumerate(hand_scores):
                player = self.get_player(i)
                if player.active and score == maximum:
                    winners.append(i)

        pot_total = self.pot_total()
        # Divide the total pot among players
        payoff = pot_total/len(winners)
        payoffs = [-p.total for p in self.players]

        # Add the payoffs to winner
        for w in winners:
            payoffs[w] += payoff

        return np.array(payoffs)

    def pot_total(self):

        #     # Maintain value of total and current raise
        #     # total = self.num_players
        #     # current_raise = 1
        #     # for h in self.history:

        #     #     # Only look to accumulate to pot if history length more than 0
        #     #     if len(h) > 0:
        #     #         for a in h:
        #     #             if a == 'R':
        #     #                 total += 2*current_raise - current_raise
        #     #                 current_raise *= 2
        #     #             if a == 'C':
        #     #                 total += current_raise
        #     #     # Reset the current raise
        #     #     current_raise = 1
        #     # return total
        total = 0
        for p in self.players:
            total += p.total
        return total

    # def bet_total(self, id):

    #     # Maintain value of total and current raise
    #     total = 1
    #     current_raise = 1
    #     for h in self.history:

    #         # Only look to accumulate to pot if history length more than 0
    #         if len(h) > 0:
    #             for i, a in enumerate(h):
    #                 current_raise *= 2
    #                 total += current_raise

    #                 total += 2*current_raise
    #                 if a == 'C':
    #                     total += current_raise
    #         current_raise = 1
    #     return total
