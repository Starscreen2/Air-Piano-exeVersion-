"""
Air-Piano - Hand Gesture MIDI Controller
Updated for Python 3.8+ compatibility using MediaPipe instead of cvzone
"""

import sys
print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
print("✅ Using MediaPipe for hand tracking (Python 3.8+ compatible)")

import cv2
import threading
import time
import numpy as np
import mediapipe as mp

# MediaPipe Hand Detection (replaces cvzone)
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
    
    def fingersUp(self, hand_data):
        """Determine which fingers are up based on landmark positions"""
        landmarks = hand_data["landmarks"]
        fingers = []
        
        # Tip and PIP landmark IDs for each finger
        tip_ids = [4, 8, 12, 16, 20]  # Thumb, Index, Middle, Ring, Pinky
        pip_ids = [3, 6, 10, 14, 18]   # PIP joints
        
        # Thumb (special case - check x-coordinate)
        if hand_data["type"] == "Right":
            fingers.append(1 if landmarks[tip_ids[0]][0] > landmarks[pip_ids[0]][0] else 0)
        else:
            fingers.append(1 if landmarks[tip_ids[0]][0] < landmarks[pip_ids[0]][0] else 0)
        
        # Other fingers (check y-coordinate - tip should be above PIP when extended)
        for i in range(1, 5):
            fingers.append(1 if landmarks[tip_ids[i]][1] < landmarks[pip_ids[i]][1] else 0)
        
        return fingers

# Try to import pygame for MIDI, but handle gracefully if no MIDI device
try:
    import pygame.midi
    pygame.midi.init()
    # Check if any MIDI devices are available
    midi_device_count = pygame.midi.get_count()
    if midi_device_count > 0:
        player = pygame.midi.Output(0)
        player.set_instrument(0)  # 0 = Acoustic Grand Piano
        MIDI_AVAILABLE = True
        print("✅ MIDI output initialized successfully!")
    else:
        MIDI_AVAILABLE = False
        print("⚠️ No MIDI devices found. Audio feedback disabled.")
except Exception as e:
    MIDI_AVAILABLE = False
    print(f"⚠️ MIDI initialization failed: {e}")
    print("💡 To enable audio, install loopMIDI from: https://www.tobias-erichsen.de/software/loopmidi.html")

# Try to import pygame for sound effects as backup
try:
    import pygame
    pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
    SOUND_AVAILABLE = True
    print("✅ Pygame mixer initialized for sound effects!")
except Exception as e:
    SOUND_AVAILABLE = False
    print(f"⚠️ Sound initialization failed: {e}")

# 🎐 Initialize Hand Detector
cap = cv2.VideoCapture(0)
detector = HandDetector(detectionCon=0.8)

# 🎺 Chord Mapping for Fingers (D Major Scale)
chords = {
    "left": {
        "thumb": [62, 66, 69],   # D Major (D, F#, A)
        "index": [64, 67, 71],   # E Minor (E, G, B)
        "middle": [66, 69, 73],  # F# Minor (F#, A, C#)
        "ring": [67, 71, 74],    # G Major (G, B, D)
        "pinky": [69, 73, 76]    # A Major (A, C#, E)
    },
    "right": {
        "thumb": [62, 66, 69],   # D Major (D, F#, A)
        "index": [64, 67, 71],   # E Minor (E, G, B)
        "middle": [66, 69, 73],  # F# Minor (F#, A, C#)
        "ring": [67, 71, 74],    # G Major (G, B, D)
        "pinky": [69, 73, 76]    # A Major (A, C#, E)
    }
}

# Chord names for display
chord_names = {
    "left": {
        "thumb": "D Major",
        "index": "E Minor", 
        "middle": "F# Minor",
        "ring": "G Major",
        "pinky": "A Major"
    },
    "right": {
        "thumb": "D Major",
        "index": "E Minor",
        "middle": "F# Minor", 
        "ring": "G Major",
        "pinky": "A Major"
    }
}

# Sustain Time (in seconds) after the finger is lowered
SUSTAIN_TIME = 2.0

# Track Previous States to Stop Chords
prev_states = {hand: {finger: 0 for finger in chords[hand]} for hand in chords}

# Track currently playing chords for display
current_chords = []

# 🎵 Function to Play a Chord
def play_chord(chord_notes, chord_name):
    if MIDI_AVAILABLE:
        for note in chord_notes:
            player.note_on(note, 127)  # Start playing
    
    # Add visual feedback
    if chord_name not in current_chords:
        current_chords.append(chord_name)
    
    print(f"🎵 Playing: {chord_name}")

# 🎵 Function to Stop a Chord After a Delay
def stop_chord_after_delay(chord_notes, chord_name):
    time.sleep(SUSTAIN_TIME)  # Sustain for specified time
    
    if MIDI_AVAILABLE:
        for note in chord_notes:
            player.note_off(note, 127)  # Stop playing
    
    # Remove from current chords display
    if chord_name in current_chords:
        current_chords.remove(chord_name)
    
    print(f"🎵 Stopped: {chord_name}")

# Function to generate a simple beep sound as fallback
def generate_beep(frequency=440, duration=0.1):
    if SOUND_AVAILABLE:
        sample_rate = 22050
        frames = int(duration * sample_rate)
        
        # Create stereo array (2 channels)
        arr = np.zeros((frames, 2))
        
        for i in range(frames):
            # Apply fade in/out to avoid clicks
            fade = min(i / (frames * 0.1), (frames - i) / (frames * 0.1), 1.0)
            wave = np.sin(2 * np.pi * frequency * i / sample_rate) * fade
            arr[i, 0] = wave  # Left channel
            arr[i, 1] = wave  # Right channel
        
        arr = (arr * 32767).astype(np.int16)
        sound = pygame.sndarray.make_sound(arr)
        sound.play()

def draw_instructions(img):
    """Draw instructions and status on the image"""
    height, width = img.shape[:2]
    
    # Semi-transparent overlay
    overlay = img.copy()
    cv2.rectangle(overlay, (10, 10), (width-10, 150), (0, 0, 0), -1)
    cv2.addWeighted(overlay, 0.7, img, 0.3, 0, img)
    
    # Instructions
    cv2.putText(img, "Air-Piano - Hand Gesture MIDI Controller", (20, 35), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    
    # Audio status
    if MIDI_AVAILABLE:
        cv2.putText(img, "🎹 MIDI Audio: ON", (20, 60), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
    else:
        cv2.putText(img, "🔇 MIDI Audio: OFF (Install loopMIDI for sound)", (20, 60), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
    
    cv2.putText(img, "Raise fingers to play chords in D Major scale", (20, 85), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    cv2.putText(img, "Thumb=D Major, Index=E Minor, Middle=F# Minor", (20, 105), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    cv2.putText(img, "Ring=G Major, Pinky=A Major | Press 'q' to quit", (20, 125), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    
    # Currently playing chords
    if current_chords:
        y_start = height - 60
        cv2.putText(img, f"🎵 Playing: {', '.join(current_chords)}", (20, y_start), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

print("🎹 Air-Piano Started!")
print("📋 Instructions:")
print("   - Raise your fingers to play chords")
print("   - Each finger maps to a different chord in D Major scale")
print("   - Press 'q' to quit")
if not MIDI_AVAILABLE:
    print("💡 For audio output, download and install loopMIDI:")
    print("   https://www.tobias-erichsen.de/software/loopmidi.html")

while True:
    success, img = cap.read()
    if not success:
        print("❌ Camera not capturing frames")
        continue

    # Flip image horizontally for mirror effect
    img = cv2.flip(img, 1)
    
    hands, img = detector.findHands(img, draw=True)

    if hands:
        for hand in hands:
            hand_type = "left" if hand["type"] == "Left" else "right"
            fingers = detector.fingersUp(hand)
            finger_names = ["thumb", "index", "middle", "ring", "pinky"]

            for i, finger in enumerate(finger_names):
                if finger in chords[hand_type]:  # Only check assigned chords
                    if fingers[i] == 1 and prev_states[hand_type][finger] == 0:
                        chord_name = chord_names[hand_type][finger]
                        play_chord(chords[hand_type][finger], chord_name)
                        
                        # Fallback beep if no MIDI
                        if not MIDI_AVAILABLE and SOUND_AVAILABLE:
                            # Different frequencies for different chords
                            frequencies = {"thumb": 262, "index": 294, "middle": 330, "ring": 349, "pinky": 392}
                            generate_beep(frequencies.get(finger, 440), 0.3)
                            
                    elif fingers[i] == 0 and prev_states[hand_type][finger] == 1:
                        chord_name = chord_names[hand_type][finger]
                        threading.Thread(target=stop_chord_after_delay, 
                                       args=(chords[hand_type][finger], chord_name), 
                                       daemon=True).start()
                    prev_states[hand_type][finger] = fingers[i]  # Update state
    else:
        # If no hands detected, stop all chords after delay
        for hand in chords:
            for finger in chords[hand]:
                if prev_states[hand][finger] == 1:  # Only if it was playing
                    chord_name = chord_names[hand][finger]
                    threading.Thread(target=stop_chord_after_delay, 
                                   args=(chords[hand][finger], chord_name), 
                                   daemon=True).start()
        prev_states = {hand: {finger: 0 for finger in chords[hand]} for hand in chords}

    # Draw instructions and status
    draw_instructions(img)
    
    cv2.imshow("Air-Piano - Hand Gesture MIDI Controller", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

if MIDI_AVAILABLE:
    pygame.midi.quit()
if SOUND_AVAILABLE:
    pygame.mixer.quit()

print("🎹 Air-Piano Stopped!")