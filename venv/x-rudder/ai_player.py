from .player import Player
from .state import State


class AIPlayer(Player):
    def __init__(self, tokens, moves):
        names = ("TARS", "Ava", "J.A.R.V.I.S", "Friday", "Christopher", "Ultron", "Samantha", "HAL 9000")
        super().__init__(choice(names), tokens, moves)

    def get_next_move(self):
        if self.tokens == 0:
            print("You no longer have tokens to place, you can try moving a token\n")
            return False
        width = randrange(0, 12, 1)
        height = randrange(0, 10, 1)
        print("({}, {})".format(width, height))
        return "1", (width, height)

    def evaluate_state(self, state):
        pass

    def get_next_possible_states(self, state):
        states = dict()

        # get all next move states
        if turn == 1:
            for w in state.width:
                for h in state.height:
                    if (w, h) not in state.p1_coordinates + state.p2_coordinates:
                        new_state = state
                        new_state.p1_coordinates.append((w, h))
                        new_state.p1_tokens -= 1
                        new_state.p1_moves -= 1

                        states["{}_{}__1".format(w, h)] = dict(state=new_state,
                                                               move_from=(-1, -1),
                                                               move_to=(w, h))

                        for i in range(w - 1, w + 1):
                            for j in range(h - 1, h + 1):
                                if i == w and j == h:
                                    continue
                                new_state = state
                                new_state.p1_coordinates.append((w, h))
                                new_state.p1_coordinates.remove((i, j))
                                new_state.p1_moves -= 1

                                states["{}_{}__{}_{}__1".format(i, j, w, h)] = dict(state=new_state,
                                                                                    move_from=(i, j),
                                                                                    move_to=(w, h))

        elif turn == 2:
            for w in state.width:
                for h in state.height:
                    if (w, h) not in state.p1_coordinates + state.p2_coordinates:
                        new_state = state
                        new_state.p2_coordinates.append((w, h))
                        new_state.p2_tokens -= 1
                        new_state.p2_moves -= 1

                        states["{}_{}__2".format(w, h)] = dict(state=new_state,
                                                               move_from=(-1, -1),
                                                               move_to=(w, h))

                        for i in range(w - 1, w + 1):
                            for j in range(h - 1, h + 1):
                                if i == w and j == h:
                                    continue
                                new_state = state
                                new_state.p2_coordinates.append((w, h))
                                new_state.p2_coordinates.remove((i, j))
                                new_state.p2_moves -= 1

                                states["{}_{}__{}_{}__2".format(i, j, w, h)] = dict(state=new_state,
                                                                                    move_from=(i, j),
                                                                                    move_to=(w, h))

        return states

    def mini_max(self, state, depth=3, is_max=True):
        if depth == 1 or state.is_terminal():
            return self.evaluate_state(state), None

        possible_states = self.get_next_possible_states(state)

        if is_max:
            best_score = -inf
        else:
            best_score = inf

        next_move = ''
        state_keys = list(possible_states.keys())

        for key in state_keys:
            child_score, child_state = self.mini_max(possible_states[key][state], depth - 1, not is_max)

            if is_max:
                if child_score > best_score:
                    best_score = child_score
                    next_move = possible_states[key]

            elif not is_max:
                if child_score < best_score:
                    best_score = child_score
                    next_move = possible_states[key]

            return best_score, next_move