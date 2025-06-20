import gymnasium as gym
from gymnasium import spaces
import numpy as np
import pygame
from brain_support import get_valid_moves, apply_move, get_winner

class ReversiEnv(gym.Env):
    metadata = {"render_modes": ["human"]}

    def __init__(self, render_mode=False):
        super().__init__()
        self.observation_space = spaces.Box(low=0, high=2, shape=(8, 8), dtype=np.int32)
        self.action_space = spaces.Discrete(64)
        self.render_mode = render_mode
        self.board = None
        self.current_player = 1
        self.window = None
        self.reset()

    def reset(self, seed=None, options=None):
        self.board = np.zeros((8, 8), dtype=np.int32)
        self.board[3][3] = 1
        self.board[4][4] = 1
        self.board[3][4] = 2
        self.board[4][3] = 2
        self.current_player = 1
        return self.board.copy(), {}

    def step(self, action):
        x, y = divmod(action, 8)
        valid_moves = get_valid_moves(self.board, self.current_player)

        # If no valid moves, pass turn to opponent
        if not valid_moves:
            self.current_player = 3 - self.current_player
            valid_moves = get_valid_moves(self.board, self.current_player)
            # If opponent also has no moves, game over
            if not valid_moves:
                done = True
                reward = 0.0
                winner = get_winner(self.board)
                if winner == 1:
                    reward = 1.0
                elif winner == 2:
                    reward = -1.0
                return self.board.copy(), reward, done, False, {}
            else:
                return self.board.copy(), 0.0, False, False, {}

        # If invalid move, penalize and end episode
        if (x, y) not in valid_moves:
            return self.board.copy(), -1.0, True, False, {}

        # Apply valid move
        self.board = apply_move(self.board, (x, y), self.current_player)

        self.current_player = 3 - self.current_player

        # Check if both players have moves left
        done = False
        if (len(get_valid_moves(self.board, 1)) == 0 and
            len(get_valid_moves(self.board, 2)) == 0):
            done = True
            winner = get_winner(self.board)
            reward = 0.0
            if winner == 1:
                reward = 1.0
            elif winner == 2:
                reward = -1.0
            else:
                reward = 0.0
            return self.board.copy(), reward, done, False, {}

        return self.board.copy(), 0.0, done, False, {}

    def render(self):
        if not self.render_mode:
            return
        if not self.window:
            pygame.init()
            self.window = pygame.display.set_mode((400, 400))
        self.window.fill((0, 128, 0))
        cell_size = 50
        for y in range(8):
            for x in range(8):
                rect = pygame.Rect(x*cell_size, y*cell_size, cell_size, cell_size)
                pygame.draw.rect(self.window, (0, 100, 0), rect, 1)
                if self.board[y][x] == 1:
                    pygame.draw.circle(self.window, (255, 255, 255), rect.center, 20)
                elif self.board[y][x] == 2:
                    pygame.draw.circle(self.window, (0, 0, 0), rect.center, 20)
        pygame.display.flip()
