import cv2
import time
import random
from game.detector import PoseDetector
from game.moves import MOVES, DIFFICULTY
from game.ui import (
    draw_move_prompt, draw_score, draw_hit,
    draw_countdown, draw_game_over, draw_round_timer,
)

# --- Settings ---
CAMERA_INDEX   = 1
FRAME_WIDTH    = 1280
FRAME_HEIGHT   = 720
ROUND_DURATION = 60       # seconds per round
DIFFICULTY     = "medium" # easy / medium / hard
TIME_PER_MOVE  = 2.0      # seconds to hit each move
HIT_DISPLAY    = 0.6      # seconds to show HIT/MISS
BASE_POINTS    = 100      # points per successful hit

def run_game():
    detector = PoseDetector()
    cap = cv2.VideoCapture(CAMERA_INDEX)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

    if not cap.isOpened():
        print("Camera not found! Check CAMERA_INDEX in main.py")
        return

    high_score = 0

    while True:
        # --- Countdown before round starts ---
        for i in range(3, 0, -1):
            start = time.time()
            while time.time() - start < 1.0:
                ret, frame = cap.read()
                if not ret:
                    continue
                frame = cv2.resize(frame, (FRAME_WIDTH, FRAME_HEIGHT))
                draw_countdown(frame, i)
                cv2.imshow('Just Box', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    cap.release()
                    cv2.destroyAllWindows()
                    return

        # --- Round state ---
        score         = 0
        combo         = 0
        round_start   = time.time()
        move_start    = time.time()
        current_move  = random.choice(list(MOVES.keys()))
        hit_result    = None   # "hit" / "miss" / None
        hit_time      = 0
        last_detected = None
        last_detect_time = 0
        DEBOUNCE      = 0.4   # seconds between detections

        print(f"\nRound started! You have {ROUND_DURATION} seconds.")
        print(f"Current move: {MOVES[current_move]['name']}")

        while True:
            ret, frame = cap.read()
            if not ret:
                continue

            frame = cv2.resize(frame, (FRAME_WIDTH, FRAME_HEIGHT))
            h, w, _ = frame.shape
            now = time.time()

            # --- Time calculations ---
            round_elapsed  = now - round_start
            round_remaining = ROUND_DURATION - round_elapsed
            move_elapsed   = now - move_start
            move_remaining = TIME_PER_MOVE - move_elapsed

            # --- Round over ---
            if round_remaining <= 0:
                break

            # --- Move timed out ---
            if move_remaining <= 0 and hit_result is None:
                hit_result = "miss"
                hit_time   = now
                combo      = 0
                print(f"MISS — {MOVES[current_move]['name']}")

            # --- After hit/miss display, pick next move ---
            if hit_result is not None and now - hit_time > HIT_DISPLAY:
                hit_result    = None
                current_move  = random.choice(list(MOVES.keys()))
                move_start    = now
                last_detected = None
                print(f"Next move: {MOVES[current_move]['name']}")

            # --- Pose detection ---
            landmarks = detector.get_landmarks(frame)

            if landmarks is not None and hit_result is None:
                detector.draw_landmarks(frame, landmarks)
                detected = detector.detect_move(landmarks, w, h)

                # debounce — ignore repeated detections too quickly
                if (detected is not None and
                    detected != last_detected or
                    now - last_detect_time > DEBOUNCE):

                    if detected == current_move:
                        combo      += 1
                        points      = BASE_POINTS * combo
                        score      += points
                        hit_result  = "hit"
                        hit_time    = now
                        last_detected = detected
                        last_detect_time = now
                        print(f"HIT! {MOVES[current_move]['name']} — +{points} pts (x{combo} combo)")

            # --- Draw UI ---
            draw_move_prompt(frame, current_move, max(move_remaining, 0), TIME_PER_MOVE)
            draw_score(frame, score, combo)
            draw_round_timer(frame, max(round_remaining, 0))

            if hit_result == "hit":
                draw_hit(frame, True)
            elif hit_result == "miss":
                draw_hit(frame, False)

            cv2.imshow('Just Box', frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                cap.release()
                cv2.destroyAllWindows()
                return

        # --- Game over screen ---
        high_score = max(score, high_score)
        print(f"\nRound over! Score: {score} | Best: {high_score}")

        while True:
            ret, frame = cap.read()
            if not ret:
                continue
            frame = cv2.resize(frame, (FRAME_WIDTH, FRAME_HEIGHT))
            draw_game_over(frame, score, high_score)
            cv2.imshow('Just Box', frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('r'):
                break
            if key == ord('q'):
                cap.release()
                cv2.destroyAllWindows()
                return

if __name__ == "__main__":
    run_game()