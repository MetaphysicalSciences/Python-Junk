import numpy as np

DIRECTIONS = [(-1, -1), (-1, 0), (-1, 1),
              (0, -1),          (0, 1),
              (1, -1),  (1, 0), (1, 1)]

def on_board(x, y):
    return 0 <= x < 8 and 0 <= y < 8

def get_valid_moves(board, player):
    moves = []
    for x in range(8):
        for y in range(8):
            if board[x][y] != 0:
                continue
            for dx, dy in DIRECTIONS:
                nx, ny = x + dx, y + dy
                found_opponent = False
                while on_board(nx, ny) and board[nx][ny] == 3 - player:
                    nx += dx
                    ny += dy
                    found_opponent = True
                if found_opponent and on_board(nx, ny) and board[nx][ny] == player:
                    moves.append((x, y))
                    break
    return moves

def apply_move(board, move, player):
    new_board = board.copy()
    x, y = move
    new_board[x][y] = player
    for dx, dy in DIRECTIONS:
        nx, ny = x + dx, y + dy
        to_flip = []
        while on_board(nx, ny) and new_board[nx][ny] == 3 - player:
            to_flip.append((nx, ny))
            nx += dx
            ny += dy
        if on_board(nx, ny) and new_board[nx][ny] == player:
            for fx, fy in to_flip:
                new_board[fx][fy] = player
    return new_board

def get_winner(board):
    p1 = np.sum(board == 1)
    p2 = np.sum(board == 2)
    if p1 > p2:
        return 1
    elif p2 > p1:
        return 2
    else:
        return 0
