# 価値が最大となる操作を常に選択したときの現在価値をベルマン方程式によって計算
def V(s, gamma=0.99):
    """価値関数

    Args:
        s: 状態
        gamma: 割引率
    Returns:
        float: ある状態sを初期条件として、指定された行動回数の下、価値が最大となる行動を選択し続けた結果として最終的に得られる価値
    """
    V = R(s) + gamma * max_V_on_next_state(s)
    print(V)
    return V


def R(s):
    """報酬関数
    Args:
        s: 状態。
    Returns:
        int: 1 (happy_endのとき)、-1 (bad_endのとき)、0（それら以外）
    """
    if s == "happy_end":
        return 1
    elif s == "bad_end":
        return -1
    else:
        return 0


def max_V_on_next_state(s):
    """
    ベルマン方程式の右辺の一部
    ある状態において取りうる各行動を取った結果として得られる価値の期待値（遷移確率と一期先の価値から計算）のうち最大の価値。
    """
    # If game end, expected value is 0.
    if s in ["happy_end", "bad_end"]:
        return 0

    actions = ["up", "down"]
    values = []
    for a in actions:
        transition_probs = transit_func(s, a)
        v = 0
        for next_state in transition_probs:
            print(next_state)
            prob = transition_probs[next_state]
            v += prob * V(next_state)
        values.append(v)
    return max(values)


def transit_func(s, a):
    """遷移関数
    現在の状態sから次に取りうる状態に遷移する確率を返す関数
    現在の状態sに次に取りうる行動aを追加して、次の状態を表す。
    下記はその例。

    Make next state by adding action str to state.
    ex: (s = 'state', a = 'up') => 'state_up'
        (s = 'state_up', a = 'down') => 'state_up_down'

    Returns:
        dict:遷移確率の辞書
    """

    actions = s.split("_")[1:]
    LIMIT_GAME_COUNT = 5
    HAPPY_END_BORDER = 4
    MOVE_PROB = 0.9

    def next_state(state, action):
        return "_".join([state, action])

    if len(actions) == LIMIT_GAME_COUNT:
        up_count = sum([1 if a == "up" else 0 for a in actions])
        state = "happy_end" if up_count >= HAPPY_END_BORDER else "bad_end"
        prob = 1.0
        # print(actions, state)
        return {state: prob}
    else:
        opposite = "up" if a == "down" else "down"
        return {next_state(s, a): MOVE_PROB, next_state(s, opposite): 1 - MOVE_PROB}


if __name__ == "__main__":
    # print(V("state"))
    # print(V("state_up_up"))
    V("state_up_up_up_up")
    # print(V("state_down_down"))
