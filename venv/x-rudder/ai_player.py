from player import Player
from state import State

from random import choice, shuffle
from math import inf
import copy


class AIPlayer(Player):
    def __init__(self, tokens, moves):
        names = ("TARS", "Ava", "J.A.R.V.I.S", "Friday", "Christopher", "Ultron", "Samantha", "HAL 9000")
        super().__init__(choice(names), tokens, moves)

    def get_next_move(self):
        if self.tokens == 0:
            print("You no longer have tokens to place, you can try moving a token\n")
            return False
        score, move = self.mini_max(AIPlayer.game_state, 2, True)
        print("Score: {}\nMove: {}".format(score, move))

        if move['move_from'] == (-1, -1):
            return "1", move['move_to']
        else:
            return "2", move['move_from'], move['move_to']

    def evaluate_state(self, state, is_max):
        max_score = 0
        min_score = 0

        w_2_max = 10
        w_3_one_cross_max = 50
        w_3_no_cross_max = 200
        w_4_one_cross_max = 1000
        w_4_no_cross_max = 1500
        w_4_blocked_max = -100
        w_5_not_crossed_max = 100000

        w_2_min = 10
        w_3_one_cross_min = 50
        w_3_no_cross_min = 500
        w_4_one_cross_min = 3000
        w_4_no_cross_min = 4500
        w_4_blocked_min = -100
        w_5_not_crossed_min = 100000

        num_2_max = 0
        num_3_one_cross_max = 0
        num_3_no_cross_max = 0
        num_4_one_cross_max = 0
        num_4_no_cross_max = 0
        num_4_blocked_max = 0
        num_5_not_crossed_max = 0

        num_2_min = 0
        num_3_one_cross_min = 0
        num_3_no_cross_min = 0
        num_4_one_cross_min = 0
        num_4_no_cross_min = 0
        num_4_blocked_min = 0
        num_5_not_crossed_min = 0

        for (x, y) in state.p2_coordinates:
            shape_size = 1
            shape_tiles = []
            num_crosses = 0

            if (x - 1, y - 1) in state.p2_coordinates:
                shape_size += 1
                shape_tiles.append((x - 1, y - 1))
            if (x + 1, y - 1) in state.p2_coordinates:
                shape_size += 1
                shape_tiles.append((x + 1, y - 1))
            if (x - 1, y + 1) in state.p2_coordinates:
                shape_size += 1
                shape_tiles.append((x - 1, y + 1))
            if (x + 1, y + 1) in state.p2_coordinates:
                shape_size += 1
                shape_tiles.append((x + 1, y + 1))

            if (x - 1, y) in state.p1_coordinates:
                num_crosses += 1
            if (x + 1, y) in state.p1_coordinates:
                num_crosses += 1

            if shape_size == 2:
                num_2_max += 1
            elif shape_size == 3:
                # Might not work, remove to fix
                if x == 0 or x == state.width - 1 or y == 0 or y == state.height - 1:
                    continue
                elif num_crosses == 0:
                    num_3_no_cross_max += 1
                elif num_crosses == 1:
                    num_3_one_cross_max += 1
            elif shape_size == 4:
                if num_crosses == 0:
                    if (x - 1, y - 1) in state.p1_coordinates \
                            or (x + 1, y - 1) in state.p1_coordinates \
                            or (x - 1, y + 1) in state.p1_coordinates \
                            or (x + 1, y + 1) in state.p1_coordinates:
                        num_4_blocked_max += 1
                    else:
                        num_4_no_cross_max += 1
                elif num_crosses == 1:
                    num_4_one_cross_max += 1
            elif shape_size == 5:
                if num_crosses != 2:
                    num_5_not_crossed_max += 1

        for (x, y) in state.p1_coordinates:
            shape_size = 1
            shape_tiles = []
            num_crosses = 0

            if (x - 1, y - 1) in state.p1_coordinates:
                shape_size += 1
                shape_tiles.append((x - 1, y - 1))
            if (x + 1, y - 1) in state.p1_coordinates:
                shape_size += 1
                shape_tiles.append((x + 1, y - 1))
            if (x - 1, y + 1) in state.p1_coordinates:
                shape_size += 1
                shape_tiles.append((x - 1, y + 1))
            if (x + 1, y + 1) in state.p1_coordinates:
                shape_size += 1
                shape_tiles.append((x + 1, y + 1))

            if (x - 1, y) in state.p2_coordinates:
                num_crosses += 1
            if (x + 1, y) in state.p2_coordinates:
                num_crosses += 1

            if shape_size == 2:
                num_2_min += 1
            elif shape_size == 3:
                # Might not work, remove to fix
                if x == 0 or x == state.height - 1 or y == 0 or y == state.width - 1:
                    continue
                elif num_crosses == 0:
                    num_3_no_cross_min += 1
                elif num_crosses == 1:
                    num_3_one_cross_min += 1
            elif shape_size == 4:
                if num_crosses == 0:
                    if (x - 1, y - 1) in state.p2_coordinates \
                            or (x + 1, y - 1) in state.p2_coordinates \
                            or (x - 1, y + 1) in state.p2_coordinates \
                            or (x + 1, y + 1) in state.p2_coordinates:
                        num_4_blocked_min += 1
                    else:
                        num_4_no_cross_min += 1
                elif num_crosses == 1:
                    num_4_one_cross_min += 1
            elif shape_size == 5:
                if num_crosses != 2:
                    num_5_not_crossed_min += 1

        max_score += (w_2_max * num_2_max +
                      w_3_one_cross_max * num_3_one_cross_max +
                      w_3_no_cross_max * num_3_no_cross_max +
                      w_4_one_cross_max * num_4_one_cross_max +
                      w_4_no_cross_max * num_4_no_cross_max +
                      w_4_blocked_max * num_4_blocked_max +
                      w_5_not_crossed_max * num_5_not_crossed_max)

        min_score += (w_2_min * num_2_min +
                      w_3_one_cross_min * num_3_one_cross_min +
                      w_3_no_cross_min * num_3_no_cross_min +
                      w_4_one_cross_min * num_4_one_cross_min +
                      w_4_no_cross_min * num_4_no_cross_min +
                      w_4_blocked_min * num_4_blocked_min +
                      w_5_not_crossed_min * num_5_not_crossed_min)

        score = 0

        if self.id == 2:
            score = max_score - min_score
        elif self.id == 1:
            score = min_score - max_score
        return score

    @staticmethod
    def get_next_possible_states(state):
        states = dict()

        # get all next move states
        if state.turn == 1:
            for w in range(state.width):
                for h in range(state.height):
                    if ((h, w) not in state.p1_coordinates + state.p2_coordinates) and state.p1_tokens > 0:
                        new_state = copy.deepcopy(state)
                        new_state.p1_coordinates.append((h, w))
                        new_state.p1_tokens -= 1
                        new_state.p1_moves -= 1

                        states["{}_{}__1".format(w, h)] = dict(state=new_state,
                                                               move_from=(-1, -1),
                                                               move_to=(h, w))
                    elif (h, w) in state.p1_coordinates:
                        left = w - 1
                        right = w + 1
                        if left < 0:
                            left = 0
                        if right >= state.width:
                            right = state.width - 1

                        down = h - 1
                        up = h + 1
                        if down < 0:
                            down = 0
                        if up >= state.height:
                            up = state.height - 1

                        for i in range(left, right):
                            for j in range(down, up):
                                if i == w and j == h:
                                    continue
                                if (j, i) not in state.p1_coordinates + state.p2_coordinates:
                                    new_state = copy.deepcopy(state)
                                    new_state.p1_coordinates.append((j, i))
                                    new_state.p1_coordinates.remove((h, w))
                                    new_state.p1_moves -= 1

                                    states["{}_{}__{}_{}__1".format(i, j, w, h)] = dict(state=new_state,
                                                                                        move_from=(h, w),
                                                                                        move_to=(j, i))

        elif state.turn == 2:
            for w in range(state.width):
                for h in range(state.height):
                    if ((h, w) not in state.p1_coordinates + state.p2_coordinates) and state.p2_tokens > 0:
                        new_state = copy.deepcopy(state)
                        new_state.p2_coordinates.append((h, w))
                        new_state.p2_tokens -= 1
                        new_state.p2_moves -= 1

                        states["{}_{}__2".format(w, h)] = dict(state=new_state,
                                                               move_from=(-1, -1),
                                                               move_to=(h, w))
                    elif (h, w) in state.p2_coordinates:
                        left = w - 1
                        right = w + 1
                        if left < 0:
                            left = 0
                        if right >= state.width:
                            right = state.width - 1

                        down = h - 1
                        up = h + 1
                        if down < 0:
                            down = 0
                        if up >= state.height:
                            up = state.height - 1

                        for i in range(left, right):
                            for j in range(down, up):
                                if i == w and j == h:
                                    continue
                                if (j, i) not in state.p1_coordinates + state.p2_coordinates:
                                    new_state = copy.deepcopy(state)
                                    new_state.p2_coordinates.append((j, i))
                                    new_state.p2_coordinates.remove((h, w))
                                    new_state.p2_moves -= 1

                                    states["{}_{}__{}_{}__2".format(i, j, w, h)] = dict(state=new_state,
                                                                                        move_from=(h, w),
                                                                                        move_to=(j, i))
        return states

    def mini_max(self, state, depth, is_max):
        if depth == 1 or state.is_terminal():
            return self.evaluate_state(state, not is_max), None

        possible_states = AIPlayer.get_next_possible_states(state)

        if is_max:
            best_score = -inf
        else:
            best_score = inf

        next_move = ''
        state_keys = list(possible_states.keys())
        shuffle(state_keys)

        for key in state_keys:
            child_score, child_state = self.mini_max(possible_states[key]['state'], depth - 1, not is_max)

            if is_max:
                if child_score > best_score:
                    best_score = child_score
                    next_move = possible_states[key]

            elif not is_max:
                if child_score < best_score:
                    best_score = child_score
                    next_move = possible_states[key]

        return best_score, next_move
