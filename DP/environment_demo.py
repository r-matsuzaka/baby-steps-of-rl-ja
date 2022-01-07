# 単純にスタートからゴール地点まで移動するためだけのプログラム

####################################### ルール #######################################
# 各ステップに置いて上下左右に1セル動くことが可能
# 各セルに移動すると報酬が与えられる。
# ゴール地点に到達するまでの総報酬を計算する
# ゴール地点が二箇所用意されている。緑(1)に到達すると+1が与えられる。赤(-1)に到達すると-1が与えられる。
# それ以外の経路では、一律マイナスの報酬-0.04が与えられる
# ブロックセル(9)またはグリッドの範囲外には移動できない。（移動しようとすると、元の状態(位置)からやり直し。）
#####################################################################################
import random

from environment import Environment


class Agent:
    def __init__(self, env):
        self.actions = env.actions

    def policy(self):
        """
        ランダムに上下左右の移動方向を選択する関数

        Returns:
            int: 1(UP), -1(DOWN) , 2(LEFT), -2(RIGHT
        """
        return random.choice(self.actions)


def main():
    """ """
    # Make grid environment.
    grid = [[0, 0, 0, 1], [0, 9, 0, -1], [0, 0, 0, 0]]
    env = Environment(grid)
    agent = Agent(env)

    # Try 10 game.
    for i in range(10):
        # Initialize position of agent.
        state = env.reset()
        print(f"#########################step{i}#########################")
        print(f"初期位置：{repr(env.agent_state)}")

        total_reward = 0
        done = False

        # 赤(1)または緑(-1)のセルに到達するまで実行する
        # 赤(1)または緑(-1)のセルに到達するとdoneはTrue (See reward_func)
        while not done:
            action = agent.policy()
            next_state, reward, done = env.step(action)
            print(f"次の移動セル:{next_state}")
            print(f"得られた報酬:{reward}")
            total_reward += reward

        print("Episode {}: Agent gets {} reward.".format(i, total_reward))


if __name__ == "__main__":
    main()
