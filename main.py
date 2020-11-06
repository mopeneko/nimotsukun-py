# にもつくん
# Author: mopeneko
#
# `p`がプレイヤー、`#`が壁、`o`が荷物、`.`がゴール。
# ゴールした荷物は`O`となる。
#
# 荷物は押すことしか出来ない。
# 操作はWASDキーで行う。

from enum import Enum
import sys

stage = """\
########
# .. p #
# oo   #
#      #
########"""
stage_width = 8
stage_height = 5
states = []
player = None


class State(Enum):
    SPACE = " "
    WALL = "#"
    PLAYER = "p"
    BLOCK = "o"
    GOAL = "."
    BLOCK_ON_GOAL = "O"


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_pos(self):
        return stage_width * self.y + self.x

    def move(self, x, y):
        self.x += x
        self.y += y


def parse_stage(stage):
    states = []

    for c in stage:
        if c != "\n":
            state = State(c)
            states.append(state)

    return states


def find_player_pos(states):
    for i, state in enumerate(states):
        if state == State.PLAYER:
            y = i // stage_width
            x = i - stage_width * y
            return x, y

    raise ValueError("player is not found in states")


def print_stage(states):
    stage = ""

    for i, state in enumerate(states):
        stage += state.value

        # Put LF when the referencing state is on the right end of the stage
        if (i+1) % stage_width == 0:
            stage += "\n"

    print(stage)


def judge_clear(states):
    for state in states:
        if state == State.BLOCK:
            return False
    return True


# The function initializes states of the game
def game_initialize():
    global states, player

    states = parse_stage(stage)

    x, y = find_player_pos(states)
    player = Player(x, y)


# The function loops until the game will be stopped
def game_main():
    print_stage(states)

    cmd = input("> ").upper()

    diff_x = 0
    diff_y = 0

    if cmd == "W":
        diff_y = -1
    elif cmd == "A":
        diff_x = -1
    elif cmd == "S":
        diff_y = 1
    elif cmd == "D":
        diff_x = 1
    elif cmd == "Q":
        sys.exit()
    else:
        print("WASDQ以外が入力されました。")
        return

    diff_target_idx = stage_width * diff_y + diff_x
    target_idx = player.get_pos() + diff_target_idx
    target = states[target_idx]

    if target == State.SPACE:
        states[player.get_pos()] = State.SPACE
        player.move(diff_x, diff_y)
        states[player.get_pos()] = State.PLAYER
    elif target == State.BLOCK:
        target_front_idx = target_idx + diff_target_idx
        target_front = states[target_front_idx]

        if target_front in (State.WALL, State.BLOCK, State.BLOCK_ON_GOAL):
            return
        elif target_front == State.GOAL:
            states[target_front_idx] = State.BLOCK_ON_GOAL
        else:
            states[target_front_idx] = State.BLOCK

        states[player.get_pos()] = State.SPACE
        player.move(diff_x, diff_y)
        states[player.get_pos()] = State.PLAYER

    if judge_clear(states):
        print_stage(states)
        print("CLEAR!")
        sys.exit()


def main():
    print("にもつくん")
    print("操作方法: [W]上へ行く [A]左へ行く [S]下へ行く [D]右へ行く [Q]終了\n")

    game_initialize()

    while True:
        game_main()


if __name__ == "__main__":
    main()
