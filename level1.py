import vizdoom as vzd
import cv2
import numpy as np
import math
from time import sleep

game = vzd.DoomGame()
game.load_config("../../scenarios/level1.cfg")
game.set_window_visible(True)
game.set_automap_buffer_enabled(True)
game.set_automap_mode(vzd.AutomapMode.WHOLE)
game.set_available_game_variables([
    vzd.GameVariable.POSITION_X,
    vzd.GameVariable.POSITION_Y,
    vzd.GameVariable.ANGLE
])
game.init()

game.new_episode()
state = game.get_state()
vars = state.game_variables
start_x = float(vars[0])
start_y = float(vars[1])
print(f"Agent starts at: ({start_x}, {start_y})")

automap = state.automap_buffer
automap = np.transpose(automap, (1, 2, 0))
map_img = cv2.cvtColor(automap, cv2.COLOR_RGB2BGR)
map_h, map_w = map_img.shape[:2]

blue_mask = cv2.inRange(map_img, np.array([5, 0, 0]), np.array([255, 30, 30]))
blue_points = np.where(blue_mask > 0)
goal_px = (int(blue_points[1][0]), int(blue_points[0][0]))
start_px = (map_w // 2, map_h // 2)
print(f"Start pixel: {start_px}  Goal pixel: {goal_px}")

# Calculate direction to goal in pixel space
dx_px = goal_px[0] - start_px[0]
dy_px = goal_px[1] - start_px[1]
goal_angle = math.degrees(math.atan2(-dy_px, dx_px))
print(f"Goal direction angle: {goal_angle:.1f} degrees")

def angle_diff(target, current):
    diff = target - current
    while diff > 180: diff -= 360
    while diff < -180: diff += 360
    return diff

print("Starting navigation — pointing toward goal...")
game.new_episode()

step = 0
max_steps = 2000

while not game.is_episode_finished() and step < max_steps:
    try:
        state = game.get_state()
        if state is None:
            break

        vars = state.game_variables
        agent_x = float(vars[0])
        agent_y = float(vars[1])
        agent_ang = float(vars[2])

        # Show live automap
        am = state.automap_buffer
        if am is not None:
            am_t = np.transpose(am, (1, 2, 0))
            am_bgr = cv2.cvtColor(am_t, cv2.COLOR_RGB2BGR)
            cv2.imshow("Live Map", am_bgr)
            cv2.waitKey(1)

        # Simple: always point toward goal angle and move forward
        turn = angle_diff(goal_angle, agent_ang)
        turn_amount = max(-8, min(8, turn * 0.4))
        game.make_action([0, 0, 0, 1, turn_amount])

        if step % 50 == 0:
            print(f"Step:{step} Agent:({agent_x:.0f},{agent_y:.0f}) Angle:{agent_ang:.0f} Turn:{turn:.0f}")

        step += 1
        sleep(0.028)

    except Exception as e:
        print(f"Error: {e}")
        break

print("Done!")
game.close()
cv2.destroyAllWindows()
