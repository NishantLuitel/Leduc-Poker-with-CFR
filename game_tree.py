class Node:
    '''
    Node class defines particular nodes for the game tree
    '''

    def __init__(self, actions):
        self.actions = actions
        self.regret_sum = {action: 0 for action in actions}
        self.strategy_sum = {action: 0 for action in actions}

    # Strategy refers to the policy that a player takes
    def strategy(self, weight):
        actions = self.actions

        # Clip the negative regret to 0
        strategy = {action: max(value, 0)
                    for action, value in self.regret_sum.items()}
        norm_sum = sum([strategy[key] for key in strategy])

        # Define probability distribuition over action by dividing with
        # normalizing value
        if norm_sum > 0:
            strategy = {key: strategy[key]/norm_sum for key in actions}
        # Use constant probability distribution if the normalizing value is 0
        else:
            num_valid = len(self.actions)
            strategy = {key: 1/num_valid for key in actions}

        # Weight is 1 initially(present) , which is degraded slowly for future
        # possible action
        self.strategy_sum = {
            key: value + strategy[key]*weight for key, value in
            self.strategy_sum.items()}

        return strategy

    # Average strategy should converge to optimal defensive strategy
    def avg_strategy(self):
        avg_strategy = {action: 0 for action in self.actions}
        norm_sum = sum([value for key, value in self.strategy_sum.items()])

        # Define probability distribuition over action by dividing with
        # normalizing value
        if norm_sum > 0:
            avg_strategy = {
                key: self.strategy_sum[key]/norm_sum for key in
                self.strategy_sum}
        # Use constant probability distribution if the normalizing value is 0
        else:
            num_valid = len(self.actions)
            avg_strategy = {key: 1/num_valid for key in self.strategy_sum}

        return avg_strategy

    def __repr__(self):
        return f'strategy_sum:{self.strategy_sum}\n regret:{self.regret_sum}\n'


class Tree():
    '''
    Implementation of game tree
    '''

    def __init__(self, num_nodes):
        self.Node = {i: Node() for i in range(num_nodes)}

    def accumulate_regrets(state):
        if state.is_terminal():
            # utility = state.utility()

        info_set = state.info_set()
