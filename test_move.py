import vizdoom as vzd
from time import sleep

game = vzd.DoomGame()
game.load_config("../../scenarios/level1.cfg")
game.set_window_visible(True)
game.set_available_game_variables([
    vzd.GameVariable.POSITION_X,
    vzd.GameVariable.POSITION_Y,
    vzd.GameVariable.ANGLE
])
game.init()
game.new_episode()

print("Testing movement...")
for i in range(50):
    state = game.get_state()
    vars = state.game_variables
    print(f"Step {i}: x={vars[0]:.0f} y={vars[1]:.0f} angle={vars[2]:.0f}")
    # Try moving forward only
    game.make_action([0, 0, 0, 1, 0])
    sleep(0.05)

game.close()
