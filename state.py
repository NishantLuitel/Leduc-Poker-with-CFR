'''
This module implements the Player , Action and State class required for
state implementation

'''

from cards import Card
from copy import deepcopy, copy


class Player():

    def __init__(self, id):
        self._id = id
        self._bets = 0
        self._active = True
        self._raised = False

    def give_card(self, card):
        if isinstance(card, Card):
            self._card = card

    @property
    def card(self):
        return self._card

    def __repr__(self):

        return 'Player({0})'.format(self._id)

    def _fold(self):
        '''
        Implementing action 'fold' by player
        '''

        # Make the player inactive if he folds
        self._active = False
        self._raised = False

    def _call(self):
        '''
        Implementing action 'call' by player
        '''

        # Increase number of bets
        self._bets += 1

    def _bet(self):
        '''
        Implementing action 'bet' by player
        '''

        # Increase number of bets
        if self._bets == 0:
            self._bets += 1

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
        return True

    def action(self, act: str):
        '''
        Take the action as given by 'act' variable
        '''

        if act == 'F':
            self._fold()
        elif act == 'R':
            self._raise()
        elif act == 'C':
            self._call()
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

        new_state = State(self.num_players, self.num_rounds, self.hand_eval)

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
                       'history': self.history}
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
            if p.id == id:
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
        info_set = f"{player.card|{self._state[1]}|{self.history[:self.round+1]}}"
        return info_set

    def succesor_state(self, action, id, update=False):
        '''
        Returns the next state, given the action for a player
        '''

        if update:
            new_state = copy(self)
        else:
            new_state = self

        active_players = new_state.num_active_players()

        # Take action
        player = new_state.get_player(id)
        player.action(action)

        # Update History
        r = new_state._state['round']
        new_state._state['history'][r].append(action)

        # Find the turn
        while(True):
            turn = (new_state._state[2]+1) % self.num_players
            if new_state.players[turn].active:
                break

        # Update turn
        new_state._state['turn'] = turn

        # Update round
        if len(new_state._state['history'][r]) - \
                new_state._state.count('Ch') == active_players:
            new_state._state['round'] += 1

            # Reset the raised variable for next round
            for p in new_state.players:
                p._raised = False

        # Return successor state
        return (new_state._state)

    # def

    def actions(self):
        '''
        Returns available actions to take for current player
        '''

        num_raises_so_far = sum([p.has_raised for p in self.players])
        round_no = self._state['round']
        history_for_round = self._state['history'][round_no]

        if num_raises_so_far == self.num_players:
            return ['F', 'C']
        else:
            if len(history_for_round) == 0 or len(history_for_round) < \
                    self.num_players and all(['Ch' in history_for_round]):
                return ['F', 'C', 'R', 'Ch']
            else:
                return ['F', 'C', 'R']

    def is_terminal(self):
        '''Determine if the current state is indeed terminal'''

        # Terminal if there is only one active player
        active_players = self.num_active_players()
        if active_players == 1:
            return True

        # Terminal if the game is in final round, and all the active players
        #  have had an action(disregarding 'Check' action)

        r = self._state['round']
        if self._state['round'] == self.num_rounds-1 and \
                len(self._state['history'][r]) - self._state.count('Ch') == \
                active_players:
            return True

        return False
