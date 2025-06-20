import pygame
import time
from reversi import ReversiEnv
from brain import Brain
from save import load_experience
from brain_support import get_valid_moves

def main():
    pygame.init()
    env = ReversiEnv(render_mode=True)
    brain1 = Brain(env)
    brain2 = Brain(env)

    memory = load_experience()
    if memory and memory.get("trained"):
        brain1.load()
        brain2.load()

    obs, _ = env.reset()
    done = False
    clock = pygame.time.Clock()

    current_brain = brain1
    current_player = 1

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                pygame.quit()
                return

        env.render()

        valid_moves = get_valid_moves(env.board, current_player)
        if not valid_moves:
            # Player must pass, switch turns
            print(f"Player {current_player} has no valid moves, passing turn.")
            current_player = 3 - current_player
            current_brain = brain2 if current_brain == brain1 else brain1
            time.sleep(1)
            continue

        action = current_brain.predict(obs)

        x, y = divmod(action, 8)
        if (x, y) not in valid_moves:
            # Invalid AI move, pick first valid move
            move = valid_moves[0]
            action = move[0]*8 + move[1]
            print(f"AI picked invalid move {(x, y)}, using {move} instead.")
        else:
            move = (x, y)

        print(f"Player {current_player} plays {move}")

        obs, reward, done, _, _ = env.step(action)

        current_brain = brain2 if current_brain == brain1 else brain1
        current_player = 3 - current_player

        time.sleep(1)  # slow down so you can watch moves
        clock.tick(30)

    # Game ended, count pieces to find winner
    from brain_support import get_winner
    winner = get_winner(env.board)
    pygame.quit()

    if winner == 1:
        print("Player 1 (White) wins!")
    elif winner == 2:
        print("Player 2 (Black) wins!")
    else:
        print("It's a draw!")

if __name__ == "__main__":
    main()
