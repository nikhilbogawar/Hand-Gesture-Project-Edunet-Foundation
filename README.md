1. Voice Control using Vosk + PyAudio

Initializes Vosk model for real-time speech recognition.
Recognizes commands like:
"close all tab" → closes tabs using Ctrl+Shift+W.
"move cursor" and "stop cursor" → toggles hand-based cursor control.
"open powerpoint" → launches PowerPoint.
"open files" → matches and opens a predefined file (ML_Unit1.pdf).
"stop" → exits the system gracefully.

2. Gesture Detection using MediaPipe Hands

Tracks hand landmarks using webcam.
Detects gestures based on landmark positions:
Fist → opens Notepad.
Index Finger Pointing → opens Camera.
Custom P Gesture → opens PowerPoint.

3. Cursor Control
When "move cursor" is spoken, index finger tip position controls the mouse cursor on screen via pyautogui.

4. Text-to-Speech Feedback
Uses pyttsx3 to speak out actions like “Fist detected - Opening Notepad”.

5. Modular Functionality
detect_letter_p() detects a gesture pattern resembling the letter P.

match_file() allows voice-to-file matching and opening based on partial command matching.

Requirements to Run:

Install these Python packages:
pip install opencv-python mediapipe pyttsx3 pyautogui vosk pyaudio
Also:
Download and extract the Vosk English Model and set its path in:
model = Model("vosk-model-en-us-0.22")
Go to this link: https://alphacephei.com/vosk/models and download and paste in the project folder.

Possible Enhancements:

Add more gestures (e.g., thumbs up/down).
Add more voice commands and dynamic file mapping using a GUI or config file.
Use threading or multiprocessing to parallelize voice and gesture inputs (improves performance).
Add feedback on-screen (e.g., which gesture/command was detected).
Save logs of user actions for training future smart assistants.