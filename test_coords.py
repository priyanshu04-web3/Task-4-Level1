import vizdoom as vzd
from time import sleep

game = vzd.DoomGame()
game.load_config("../../scenarios/level1.cfg")
game.set_window_visible(False)
game.set_available_game_variables([
    vzd.GameVariable.POSITION_X,
    vzd.GameVariable.POSITION_Y,
    vzd.GameVariable.ANGLE
])
game.init()
game.new_episode()

for i in range(100):
    state = game.get_state()
    vars = state.game_variables
    x, y = float(vars[0]), float(vars[1])
    if i % 10 == 0:
        print(f"Step {i}: x={x:.1f} y={y:.1f}")
    game.make_action([0, 0, 0, 1, 0])
    sleep(0.02)

game.close()
print("Done.")
