# Air-Piano🎹:

Control MIDI piano chords in real-time using hand gestures- The webcam detects your hands in real-time using MediaPipe's hand detection.
- Each finger corresponds to a specific chord (left and right hands are mapped identically).
- When a finger is raised, a chord is played using pygame's MIDI functionality.
- When the finger is lowered, the chord sustains for a short delay before stopping.tured from your webcam. Each finger is mapped to a chord in the D major scale, and chords play and sustain naturally as you move your fingers.

**Updated for Python 3.8+ compatibility using MediaPipe instead of cvzone**

---

## 📦 Features

- 🖐️ Real-time hand detection using [MediaPipe](https://mediapipe.dev/) (Python 3.8+ compatible)
- 🎼 Chord mapping to fingers (D major scale)  
- 🎹 MIDI output with sustain effect using `pygame.midi`
- 👏 Supports both left and right hands
- 🎶 Dynamic gesture-based music interaction

---

## 🚀 Getting Started

### 1. Python Requirements
- **Python 3.8+** (tested on 3.8, 3.9, 3.10, 3.11, 3.12+)

### 2. Install Dependencies

**Option A: Quick Install**
```bash
pip install opencv-python pygame mediapipe numpy
```

**Option B: Automated Setup**
```bash
python setup.py
```

**Option C: From requirements.txt**
```bash
pip install -r requirements.txt
```

### 3. Run Air-Piano

**Option A: Direct Run**
```bash
python air_piano_main.py
```

**Option B: Test Hand Detection First**
```bash
python test_hand_detection.py
```

### 4. Build Executable (Optional)

You can create a standalone executable (.exe) that doesn't require Python to be installed:

**Build the executable:**
```bash
python build_exe.py
```

This will:
- Install PyInstaller if not already installed
- Create a single executable file in the `dist/` folder
- Generate a convenient launcher batch file (`Run-Air-Piano.bat`)

**Run the executable:**
- Double-click `Run-Air-Piano.bat` (recommended)
- Or run `dist/Air-Piano.exe` directly

> **Note:** The executable will be larger (~200MB) as it includes all dependencies, but it can run on any Windows computer without Python installed.

---

## 🎛️ How It Works

- The webcam detects your hands in real-time using `cvzone`’s `HandDetector`.
- Each finger corresponds to a specific chord (left and right hands are mapped identically).
- When a finger is raised (`fingersUp`), a chord is played.
- When the finger is lowered, the chord sustains for a short delay before stopping.

### 🎵 Chord Mapping (D Major Scale)

| Finger  | Chord (Notes)        | Description        |
|---------|----------------------|--------------------|
| Thumb   | D Major (62, 66, 69) | D - F# - A          |
| Index   | E Minor (64, 67, 71) | E - G - B           |
| Middle  | F# Minor (66, 69, 73)| F# - A - C#         |
| Ring    | G Major (67, 71, 74) | G - B - D           |
| Pinky   | A Major (69, 73, 76) | A - C# - E          |

Both hands use the same chord mapping.

---

## 🧠 Code Overview

- `pygame.midi.init()` initializes MIDI output.
- MediaPipe handles hand and finger tracking.
- Finger positions are analyzed to determine which fingers are raised.
- MIDI notes are triggered with `note_on` and `note_off` functions.
- Chords are sustained for a configurable delay (`SUSTAIN_TIME = 2.0`).

---

## 💡 Customization

- 🔁 **Change Instrument**:  
  Modify the instrument using:
  ```python
  player.set_instrument(<instrument_number>)
  ```
  Refer to the [General MIDI Instrument List](https://www.midi.org/specifications-old/item/gm-level-1-sound-set) for codes.

- 🎼 **Change Chord Scale**:  
  Replace the `chords` dictionary with your preferred scales or custom mappings.

- ⏱️ **Adjust Sustain Time**:  
  Modify `SUSTAIN_TIME` (in seconds) to lengthen or shorten the delay after chord release.

---

## 🔧 Troubleshooting

### Build Issues
- **PyInstaller not found**: The build script will automatically install PyInstaller
- **Large executable size**: This is normal (~200MB) due to included dependencies
- **Missing modules**: The build script includes all necessary dependencies

### Runtime Issues
- **Camera not detected**: Ensure your webcam is connected and not used by other applications
- **No sound**: Check that your system has MIDI capability or install a software synthesizer
- **Hand detection not working**: Ensure good lighting and clear hand visibility

---

## 📁 Project Structure

```
Air-Piano/
├── air_piano_main.py          # Main application file
├── build_exe.py               # Executable build script
├── test_hand_detection.py     # Hand detection test
├── requirements.txt           # Python dependencies
├── README.md                  # This file
├── Run-Air-Piano.bat         # Launcher (created after build)
├── dist/                     # Executable output (created after build)
│   └── Air-Piano.exe         # Standalone executable
└── build/                    # Build artifacts (created after build)
```

---

## 🛑 Exit Instructions

- Press `q` on your keyboard to quit the application safely.
- This releases the webcam and MIDI resources.

---

## 🤝 Credits

- [MediaPipe](https://mediapipe.dev/) for hand detection and tracking
- `pygame.midi` for MIDI interfacing
- OpenCV for real-time camera input

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).

---
