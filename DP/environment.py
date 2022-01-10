from enum import Enum

import numpy as np


class State:
    """状態（位置）を定義するクラス
    原点は左上
    正の向き
        -->
        ↓

    """

    def __init__(self, row=-1, column=-1):
        self.row = row
        self.column = column

    def __repr__(self):
        return "<State: [{}, {}]>".format(self.row, self.column)

    def clone(self):
        """
        （現在の）状態(位置)を返す関数

        Returns:
            Stateクラス
        """
        return State(self.row, self.column)

    def __hash__(self):
        return hash((self.row, self.column))

    def __eq__(self, other):
        return self.row == other.row and self.column == other.column


class Action(Enum):
    """行動を定義するクラス"""

    UP = 1
    DOWN = -1
    LEFT = 2
    RIGHT = -2


class Environment:
    """環境を定義するクラス"""

    def __init__(self, grid, move_prob=0.8):
        # grid is 2d-array. Its values are treated as an attribute.
        # Kinds of attribute is following.
        #  0: ordinary cell
        #  -1: damage cell (game end)
        #  1: reward cell (game end)
        #  9: block cell (can't locate agent)
        self.grid = grid
        self.agent_state = State()

        # Default reward is minus. Just like a poison swamp.
        # It means the agent has to reach the goal fast!
        self.default_reward = -0.04

        # Agent can move to a selected direction in move_prob.
        # It means the agent will move different direction
        # in (1 - move_prob).
        self.move_prob = move_prob  # 同一方向
        self.reset()

    @property
    def row_length(self):
        """
        行数を返す関数

        Returns:
            int: 行数
        """
        return len(self.grid)

    @property
    def column_length(self):
        """
        列数を返す関数

        Returns:
            int: 列数
        """
        return len(self.grid[0])

    @property
    def actions(self):
        """
        一連の行動を返す関数

        Returns:
            List: 行動のリスト
        """
        return [Action.UP, Action.DOWN, Action.LEFT, Action.RIGHT]

    @property
    def states(self):
        """
        グリッド内のすべてのセルの状態(位置)を返す関数
        ただし、ブロックセルは除く

        Returns:
            List: 各セルの状態(位置)のリスト
        """
        states = []
        for row in range(self.row_length):
            for column in range(self.column_length):
                # Block cells are not included to the state.
                if self.grid[row][column] != 9:
                    states.append(State(row, column))
        return states

    def transit_func(self, state, action):
        """遷移関数
        次に移動し得る可能性の各グリッドの遷移確率を返す関数
        関数transitに呼び出される
        Args:
            state: 現在の位置
            action: 移動を選択する方向
        Returns:
            dict: 次に移動し得る可能性の各グリッドの遷移確率
                - ゴール地点にいるとき -> {}
                - ゴール地点にいないとき、{次の位置:遷移確率、...}
        """
        transition_probs = {}
        if not self.can_action_at(state):
            # Already on the terminal cell.
            return transition_probs

        opposite_direction = Action(action.value * -1)

        for a in self.actions:
            # 選択した方向の真逆の場合
            prob = 0

            # 選択した方向の場合
            if a == action:
                prob = self.move_prob

            # 選択した方向の真逆でない場合
            # 進行方向に対して、右か左
            elif a != opposite_direction:
                prob = (1 - self.move_prob) / 2

            next_state = self._move(state, a)

            if next_state not in transition_probs:

                transition_probs[next_state] = prob

            else:
                transition_probs[next_state] += prob

        return transition_probs

    def can_action_at(self, state):
        """
        セルが0（移動可能なセル）かどうかを確認する関数

        Returns:
            bool: 0ならTrue, 0以外ならFalse
        """
        if self.grid[state.row][state.column] == 0:
            return True
        else:
            return False

    def _move(self, state, action):
        """
        現在の状態から選択した方向に移動する関数
        ただし、範囲外またはブロックセルの場合は現在の位置を返す

        Args:
            state: 現在の位置
            action: 移動を選択する方向
        Returns:
            Stete: 現在の位置からの移動後の位置
        """
        if not self.can_action_at(state):
            raise Exception("Can't move from here!")

        next_state = state.clone()

        # Execute an action (move).
        # 正の向きに注意
        if action == Action.UP:
            next_state.row -= 1
        elif action == Action.DOWN:
            next_state.row += 1
        elif action == Action.LEFT:
            next_state.column -= 1
        elif action == Action.RIGHT:
            next_state.column += 1

        # Check whether a state is out of the grid.
        # 範囲外の場合は、移動前の状態のままにする
        if not (0 <= next_state.row < self.row_length):
            print("範囲外に移動しようとしました")
            next_state = state
        if not (0 <= next_state.column < self.column_length):
            print("範囲外に移動しようとしました")
            next_state = state

        # Check whether the agent bumped a block cell.
        # ブロックセルの場合は、移動前の状態のままにする
        if self.grid[next_state.row][next_state.column] == 9:
            print("ブロックセルに移動しようとしました")
            next_state = state

        return next_state

    def reward_func(self, state):
        """報酬関数
        Args:
            state(State()): 状態(位置)
        Returns:
            float: 報酬。緑セル(1)なら+1を与える。赤セル(-1)なら-1を与える
            bool:緑または赤セルにいる場合はTrue。それ以外の場合はFalse。
        """
        # ゴール（赤or緑セル）以外のセルのときはデフォルトの報酬を与える
        reward = self.default_reward
        done = False

        # Check an attribute of next state.
        attribute = self.grid[state.row][state.column]
        if attribute == 1:
            # Get reward! and the game ends.
            reward = 1
            done = True
        elif attribute == -1:
            # Get damage! and the game ends.
            reward = -1
            done = True

        return reward, done

    def reset(self):
        """
        初期状態（位置）を返す関数

        Returns:
            State: 初期状態（位置）
        """
        # Locate the agent at lower left corner.
        self.agent_state = State(self.row_length - 1, 0)
        return self.agent_state

    def step(self, action):
        """ """
        next_state, reward, done = self.transit(self.agent_state, action)
        if next_state is not None:
            self.agent_state = next_state

        return next_state, reward, done

    def transit(self, state, action):
        """

        Args:
            State: 現在の位置
            action: エージェントがランダムに決定した進行方向（実際の移動方向とは異なる）
        Returns:
            State: 次の位置
            float: 次の位置で得られる報酬
            bool: 次の位置がゴールの場合にTrue、それ以外の場合にFalse
        """
        transition_probs = self.transit_func(state, action)
        if len(transition_probs) == 0:
            return None, None, True

        next_states = []
        probs = []
        for s in transition_probs:
            next_states.append(s)
            probs.append(transition_probs[s])

        # 次の移動する可能性のある各セルの遷移確率に基づいて、次の移動先を選択
        next_state = np.random.choice(next_states, p=probs)
        reward, done = self.reward_func(next_state)
        return next_state, reward, done
