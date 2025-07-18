import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import time
from collections import deque

class GestureControl:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            max_num_hands=2,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )
        self.mp_drawing = mp.solutions.drawing_utils
        self.is_running = False
        self.is_paused = False
        self.screen_width, self.screen_height = pyautogui.size()
        
        # Smoothing parameters
        self.cursor_smoothing = 3  # Number of frames to average for cursor position
        self.position_history = deque(maxlen=self.cursor_smoothing)
        
        # Gesture timing parameters
        self.last_click_time = 0
        self.click_delay = 0.5  # seconds between clicks
        self.last_gesture_time = 0
        self.gesture_delay = 0.3  # seconds between gestures
        
        # Thresholds
        self.click_distance_threshold = 0.05
        self.scroll_distance_threshold = 0.05
        self.swipe_threshold = 0.15  # How much movement needed for swipe
        self.swipe_duration = 0.3  # How long swipe gesture must be held

    def start(self):
        self.is_running = True
        cap = cv2.VideoCapture(0)
        
        # For swipe detection
        swipe_start_pos = None
        swipe_start_time = 0
        current_swipe_direction = None

        while self.is_running and cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.flip(frame, 1)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.hands.process(rgb_frame)

            if not self.is_paused and results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    self.mp_drawing.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                    
                    # Get current hand position
                    index_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
                    current_pos = (index_tip.x, index_tip.y)
                    
                    # Smooth cursor movement
                    self.position_history.append(current_pos)
                    smoothed_pos = np.mean(self.position_history, axis=0)
                    x = int(smoothed_pos[0] * self.screen_width)
                    y = int(smoothed_pos[1] * self.screen_height)
                    
                    # Move cursor with smoothing
                    pyautogui.moveTo(x, y, duration=0.05)
                    
                    # Detect gestures
                    current_time = time.time()
                    if current_time - self.last_gesture_time > self.gesture_delay:
                        if self.is_click_gesture(hand_landmarks):
                            if current_time - self.last_click_time > self.click_delay:
                                pyautogui.click()
                                self.last_click_time = current_time
                                self.last_gesture_time = current_time
                                cv2.putText(frame, "CLICK", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                        
                        elif self.is_scroll_gesture(hand_landmarks):
                            scroll_amount = self.get_scroll_amount(hand_landmarks)
                            pyautogui.scroll(scroll_amount)
                            self.last_gesture_time = current_time
                            cv2.putText(frame, f"SCROLL: {scroll_amount}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                        
                        elif self.is_swipe_gesture(hand_landmarks):
                            direction = self.get_swipe_direction(hand_landmarks)
                            if direction == "left":
                                pyautogui.hotkey('alt', 'left')
                                cv2.putText(frame, "SWIPE LEFT", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                            elif direction == "right":
                                pyautogui.hotkey('alt', 'right')
                                cv2.putText(frame, "SWIPE RIGHT", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                            self.last_gesture_time = current_time
                        
                        elif self.is_peace_sign(hand_landmarks):
                            pyautogui.hotkey('win', 'up')
                            self.last_gesture_time = current_time
                            cv2.putText(frame, "PEACE SIGN - MAXIMIZE", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                        
                        elif self.is_fist_gesture(hand_landmarks):
                            pyautogui.hotkey('alt', 'f4')
                            self.last_gesture_time = current_time
                            cv2.putText(frame, "FIST - CLOSE WINDOW", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # Display status
            status = "PAUSED" if self.is_paused else "ACTIVE"
            cv2.putText(frame, f"Status: {status}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(frame, "Press 'p' to Pause/Resume, 'q' to Quit", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            cv2.imshow("Gesture Control", frame)

            key = cv2.waitKey(10) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('p'):
                self.is_paused = not self.is_paused

        cap.release()
        cv2.destroyAllWindows()

    def is_click_gesture(self, hand_landmarks):
        """Improved click detection with distance threshold."""
        thumb_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.THUMB_TIP]
        index_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
        distance = self.calculate_distance(thumb_tip, index_tip)
        return distance < self.click_distance_threshold

    def is_scroll_gesture(self, hand_landmarks):
        """Detect scroll gesture with thumb and middle finger."""
        thumb_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.THUMB_TIP]
        middle_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
        distance = self.calculate_distance(thumb_tip, middle_tip)
        return distance < self.scroll_distance_threshold

    def get_scroll_amount(self, hand_landmarks):
        """Calculate scroll amount based on finger position."""
        middle_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
        middle_mcp = hand_landmarks.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_MCP]
        
        # Vertical distance between tip and MCP determines scroll speed
        vertical_diff = middle_mcp.y - middle_tip.y
        scroll_amount = int(vertical_diff * 20)  # Scale to appropriate scroll amount
        
        # Limit scroll amount
        return max(-10, min(10, scroll_amount))

    def is_swipe_gesture(self, hand_landmarks):
        """Detect if a swipe gesture is being made."""
        wrist = hand_landmarks.landmark[self.mp_hands.HandLandmark.WRIST]
        thumb_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.THUMB_TIP]
        
        # Check if thumb is extended (not touching other fingers)
        index_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
        distance = self.calculate_distance(thumb_tip, index_tip)
        return distance > self.click_distance_threshold * 2

    def get_swipe_direction(self, hand_landmarks):
        """Determine swipe direction based on hand orientation."""
        wrist = hand_landmarks.landmark[self.mp_hands.HandLandmark.WRIST]
        index_mcp = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_MCP]
        
        # Calculate hand orientation
        horizontal_diff = wrist.x - index_mcp.x
        
        if horizontal_diff < -self.swipe_threshold:
            return "left"
        elif horizontal_diff > self.swipe_threshold:
            return "right"
        return None

    def is_peace_sign(self, hand_landmarks):
        """More reliable peace sign detection."""
        tips = [
            self.mp_hands.HandLandmark.INDEX_FINGER_TIP,
            self.mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
            self.mp_hands.HandLandmark.RING_FINGER_TIP,
            self.mp_hands.HandLandmark.PINKY_TIP
        ]
        dips = [
            self.mp_hands.HandLandmark.INDEX_FINGER_DIP,
            self.mp_hands.HandLandmark.MIDDLE_FINGER_DIP,
            self.mp_hands.HandLandmark.RING_FINGER_DIP,
            self.mp_hands.HandLandmark.PINKY_DIP
        ]
        
        # Check if index and middle fingers are extended
        index_extended = hand_landmarks.landmark[tips[0]].y < hand_landmarks.landmark[dips[0]].y
        middle_extended = hand_landmarks.landmark[tips[1]].y < hand_landmarks.landmark[dips[1]].y
        
        # Check if ring and pinky fingers are folded
        ring_folded = hand_landmarks.landmark[tips[2]].y > hand_landmarks.landmark[dips[2]].y
        pinky_folded = hand_landmarks.landmark[tips[3]].y > hand_landmarks.landmark[dips[3]].y
        
        return index_extended and middle_extended and ring_folded and pinky_folded

    def is_fist_gesture(self, hand_landmarks):
        """More reliable fist detection."""
        tips = [
            self.mp_hands.HandLandmark.THUMB_TIP,
            self.mp_hands.HandLandmark.INDEX_FINGER_TIP,
            self.mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
            self.mp_hands.HandLandmark.RING_FINGER_TIP,
            self.mp_hands.HandLandmark.PINKY_TIP
        ]
        mcp_joints = [
            self.mp_hands.HandLandmark.THUMB_MCP,
            self.mp_hands.HandLandmark.INDEX_FINGER_MCP,
            self.mp_hands.HandLandmark.MIDDLE_FINGER_MCP,
            self.mp_hands.HandLandmark.RING_FINGER_MCP,
            self.mp_hands.HandLandmark.PINKY_MCP
        ]
        
        # Check if all fingertips are close to their MCP joints
        all_folded = True
        for tip, mcp in zip(tips, mcp_joints):
            if self.calculate_distance(hand_landmarks.landmark[tip], hand_landmarks.landmark[mcp]) > 0.1:
                all_folded = False
                break
                
        return all_folded

    @staticmethod
    def calculate_distance(point1, point2):
        """Calculate Euclidean distance between two points."""
        return ((point1.x - point2.x)**2 + (point1.y - point2.y)**2)**0.5

    def stop(self):
        self.is_running = False


if __name__ == "__main__":
    controller = GestureControl()
    controller.start()