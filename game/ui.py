import cv2
import time
from game.moves import MOVES

# Colors (BGR)
WHITE   = (255, 255, 255)
BLACK   = (0, 0, 0)
GREEN   = (0, 255, 0)
RED     = (0, 0, 255)
YELLOW  = (0, 255, 255)
GRAY    = (50, 50, 50)

def draw_background(frame):
    overlay = frame.copy()
    cv2.rectangle(overlay, (0, 0), (frame.shape[1], frame.shape[0]), BLACK, -1)
    cv2.addWeighted(overlay, 0.3, frame, 0.7, 0, frame)

def draw_move_prompt(frame, move_number, time_left, total_time):
    h, w, _ = frame.shape
    move = MOVES[move_number]

    # background bar at top
    cv2.rectangle(frame, (0, 0), (w, 120), GRAY, -1)

    # move number (big)
    cv2.putText(frame, str(move_number), (30, 90),
                cv2.FONT_HERSHEY_SIMPLEX, 3.0, move["color"], 5)

    # move name
    cv2.putText(frame, move["name"], (130, 55),
                cv2.FONT_HERSHEY_SIMPLEX, 1.2, WHITE, 2)

    # target (head/body)
    target_color = YELLOW if move["target"] == "head" else (0, 165, 255)
    cv2.putText(frame, move["target"].upper(), (130, 95),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, target_color, 2)

    # timer bar
    bar_width = int((time_left / total_time) * (w - 40))
    bar_color = GREEN if time_left > total_time * 0.5 else YELLOW if time_left > total_time * 0.25 else RED
    cv2.rectangle(frame, (20, 108), (20 + bar_width, 118), bar_color, -1)

def draw_score(frame, score, combo):
    h, w, _ = frame.shape

    # score top right
    cv2.putText(frame, f"Score: {score}", (w - 220, 45),
                cv2.FONT_HERSHEY_SIMPLEX, 1.0, WHITE, 2)

    # combo below score
    if combo > 1:
        combo_color = YELLOW if combo < 5 else (0, 165, 255) if combo < 10 else RED
        cv2.putText(frame, f"x{combo} COMBO", (w - 220, 85),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, combo_color, 2)

def draw_hit(frame, success):
    h, w, _ = frame.shape
    if success:
        cv2.putText(frame, "HIT!", (w // 2 - 60, h // 2),
                    cv2.FONT_HERSHEY_SIMPLEX, 2.5, GREEN, 5)
    else:
        cv2.putText(frame, "MISS", (w // 2 - 60, h // 2),
                    cv2.FONT_HERSHEY_SIMPLEX, 2.5, RED, 5)

def draw_countdown(frame, number):
    h, w, _ = frame.shape
    cv2.putText(frame, str(number), (w // 2 - 40, h // 2 + 40),
                cv2.FONT_HERSHEY_SIMPLEX, 5.0, YELLOW, 8)

def draw_game_over(frame, score, high_score):
    h, w, _ = frame.shape
    cv2.rectangle(frame, (w//2 - 200, h//2 - 120), (w//2 + 200, h//2 + 140), GRAY, -1)
    cv2.putText(frame, "ROUND OVER", (w//2 - 160, h//2 - 70),
                cv2.FONT_HERSHEY_SIMPLEX, 1.2, WHITE, 3)
    cv2.putText(frame, f"Score: {score}", (w//2 - 100, h//2 - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 1.2, GREEN, 3)
    cv2.putText(frame, f"Best:  {high_score}", (w//2 - 100, h//2 + 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1.0, YELLOW, 2)
    cv2.putText(frame, "R to restart  Q to quit", (w//2 - 180, h//2 + 110),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, WHITE, 2)

def draw_round_timer(frame, time_remaining):
    h, w, _ = frame.shape
    seconds = int(time_remaining)
    cv2.putText(frame, f"{seconds}s", (w // 2 - 30, 45),
                cv2.FONT_HERSHEY_SIMPLEX, 1.0, WHITE, 2)

def draw_landmarks(frame, landmarks, w, h):
    points = []
    for lm in landmarks:
        x, y = int(lm.x * w), int(lm.y * h)
        points.append((x, y))
        cv2.circle(frame, (x, y), 5, GREEN, -1)

    # draw connections between key joints
    connections = [
        (11, 12), (11, 13), (13, 15),
        (12, 14), (14, 16), (11, 23),
        (12, 24), (23, 24)
    ]
    for a, b in connections:
        if a < len(points) and b < len(points):
            cv2.line(frame, points[a], points[b], (0, 200, 0), 2)