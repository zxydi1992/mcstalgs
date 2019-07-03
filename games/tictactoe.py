from enum import IntEnum


class Player(IntEnum):
    cross = 1
    nought = 2


class BoardItem(IntEnum):
    empty = 0
    cross = 1
    nought = 2


class BoardState(object):

    def __init__(self):
        self.array = [[BoardItem.empty for _ in range(3)] for _ in range(3)]

    def __getitem__(self, position):
        assert isinstance(position, tuple) and len(position) == 2
        r, c = position
        return self.array[r][c]

    def __setitem__(self, position, value):
        assert isinstance(position, tuple) and len(position) == 2 and isinstance(value, BoardItem)
        r, c = position
        self.array[r][c] = value


def check(board_state: BoardState, row: int, col: int):
    value = board_state[row, col]
    if all(board_state[row, j] == value for j in range(3)):
        return True
    if all(board_state[i, col] == value for i in range(3)):
        return True
    if all(board_state[i, i] == value for i in range(3)):
        return True
    if all(board_state[i, 2 - i] == value for i in range(3)):
        return True
    return False


class TicTacTeo(object):

    def __init__(self):
        self._board_state = None
        self.current_player = None
        self.winner = None
        self.end = None

        self.reset()

    @property
    def board_state(self):
        return self._board_state

    @board_state.setter
    def board_state(self, new_state: BoardState):
        assert isinstance(new_state, BoardState)
        self._board_state = new_state

    def step(self, player: Player, position, value, strict: bool=True):
        assert (isinstance(player, Player) and isinstance(position, tuple) and
                len(position) == 2 and isinstance(value, BoardItem))
        if strict:
            assert not self.end
            assert player == value
            assert self._board_state[position] == BoardItem.empty
        self._board_state[position] = value
        if self.check_win(position):
            self.end = True
            self.winner = player
            self.current_player = None
        else:
            self.current_player = Player.cross if self.current_player == Player.nought else Player.nought

    def reset(self):
        self.current_player = Player.cross
        self.winner = None
        self.end = False
        self._board_state = BoardState()

    def check_win(self, position):
        return check(self._board_state, position[0], position[1])


if __name__ == '__main__':
    game = TicTacTeo()
    game.step(Player.cross, (1, 1), BoardItem.cross)
    print(game.board_state.array)
    game.step(Player.cross, (1, 2), BoardItem.cross, False)
    print(game.board_state.array)
    game.step(Player.cross, (1, 0), BoardItem.cross, False)
    print(game.board_state.array)
    print(game.current_player)
    print(game.winner)
    print(game.end)
