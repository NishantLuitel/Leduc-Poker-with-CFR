import numpy as np


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
        self.node_map = {i: {} for i in range(num_nodes)}
        self.action_map = {i: {} for i in range(num_nodes)}

    # def print_map(self):
    #     print(self.node_map)

    def accumulate_regrets(self, state, weights):
        if state.is_terminal():
            # pass
            utility = state.utility()
            # print("utility:", utility)
            return utility

        turn = state.state['turn']
        info_set = state.info_set(turn)
        actions = state.actions()

        if info_set not in self.action_map[turn]:
            self.action_map[turn][info_set] = actions

        if info_set not in self.node_map[turn]:
            # print('action in node_map', actions)
            self.node_map[turn][info_set] = Node(actions)

        # Find the node and extract strategy from it
        node = self.node_map[turn][info_set]
        strategy = node.strategy(weights[turn])
        # print("strategy:", strategy)

        utility = {a: 0 for a in actions}
        node_utility = np.zeros(len(self.node_map))

        # print("actions", actions)
        for action in actions:
            new_weights = [p if i != turn else p*strategy[action]
                           for i, p in enumerate(weights)]
            # print("action:", action)
            # print("node_map:", self.node_map)
            # print("action_map:", self.action_map)
            new_state = state.succesor_state(
                action, id=turn, update=False, return_object=True)
            r = self.accumulate_regrets(new_state, new_weights)
            utility[action] = r[turn]
            node_utility += r*strategy[action]

        reach_prob = 1
        for p, w in enumerate(weights):
            if p != turn:
                reach_prob *= w

        for action in actions:
            regret = utility[action] - node_utility[turn]
            node.regret_sum[action] += regret*reach_prob

        return node_utility
