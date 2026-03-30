import vizdoom as vzd
import cv2

game = vzd.DoomGame()
game.load_config("../../scenarios/level1.cfg")

# Override config settings
game.set_window_visible(True)
game.set_automap_buffer_enabled(True)
game.set_automap_mode(vzd.AutomapMode.WHOLE)

# Add ANGLE to existing variables
game.set_available_game_variables([
    vzd.GameVariable.POSITION_X,
    vzd.GameVariable.POSITION_Y,
    vzd.GameVariable.ANGLE
])

game.init()
print("Game initialized.")

game.new_episode()
state = game.get_state()
print("Agent Position:", state.game_variables)

automap = state.automap_buffer
if automap is None:
    print("Automap is None")
else:
    print("Automap shape:", automap.shape)
    map_img = cv2.cvtColor(automap, cv2.COLOR_RGB2BGR)
    cv2.imwrite("map_captured.png", map_img)
    print("Map saved as map_captured.png!")
    cv2.imshow("Map", map_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

game.close()
print("Done.")