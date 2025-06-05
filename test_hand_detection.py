"""
Test script for Air-Piano hand detection
This will verify that the MediaPipe hand detection is working correctly
"""
import cv2
import mediapipe as mp
import sys

print(f"Testing Air-Piano with Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")

# MediaPipe Hand Detection
class HandDetector:
    def __init__(self, detectionCon=0.8):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=detectionCon,
            min_tracking_confidence=0.5
        )
        self.mp_draw = mp.solutions.drawing_utils
    
    def findHands(self, img, draw=True):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.hands.process(img_rgb)
        hands_data = []
        
        if results.multi_hand_landmarks:
            for hand_idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
                if draw:
                    self.mp_draw.draw_landmarks(img, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                
                # Get hand type (Left/Right)
                hand_type = results.multi_handedness[hand_idx].classification[0].label
                
                # Extract landmark positions
                landmarks = []
                for landmark in hand_landmarks.landmark:
                    h, w, c = img.shape
                    cx, cy = int(landmark.x * w), int(landmark.y * h)
                    landmarks.append([cx, cy])
                
                hands_data.append({
                    "type": hand_type,
                    "landmarks": landmarks
                })
        
        return hands_data, img

# Test the hand detection
print("✅ Starting hand detection test...")
print("📷 Initializing camera...")

try:
    cap = cv2.VideoCapture(0)
    detector = HandDetector(detectionCon=0.8)
    
    print("✅ Camera initialized successfully!")
    print("👋 Show your hand to the camera")
    print("Press 'q' to quit test")
    
    frame_count = 0
    detection_count = 0
    
    while True:
        success, img = cap.read()
        if not success:
            print("❌ Camera not capturing frames")
            break
        
        frame_count += 1
        img = cv2.flip(img, 1)  # Mirror effect
        
        hands, img = detector.findHands(img, draw=True)
        
        if hands:
            detection_count += 1
            cv2.putText(img, f"Hands detected: {len(hands)}", (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            for i, hand in enumerate(hands):
                cv2.putText(img, f"{hand['type']} hand", (10, 70 + i*40), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
        else:
            cv2.putText(img, "No hands detected", (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        
        # Show detection rate
        if frame_count > 0:
            detection_rate = (detection_count / frame_count) * 100
            cv2.putText(img, f"Detection rate: {detection_rate:.1f}%", (10, 120), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        cv2.imshow("Air-Piano Hand Detection Test", img)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
    
    print(f"✅ Test completed!")
    print(f"📊 Detection rate: {detection_rate:.1f}% ({detection_count}/{frame_count} frames)")
    print("🎹 Your Air-Piano is ready to use!")
    
except Exception as e:
    print(f"❌ Test failed: {e}")
    print("💡 Make sure your camera is connected and not being used by another application")
