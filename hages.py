import cv2
import mediapipe as mp
import pyttsx3
import json
import os
import difflib
import pyautogui
import time
from vosk import Model, KaldiRecognizer
import pyaudio

# Voice setup
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

# Load Vosk model
model = Model("vosk-model-en-us-0.22")
recognizer = KaldiRecognizer(model, 16000)
mic = pyaudio.PyAudio()
stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
stream.start_stream()

# MediaPipe hands
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands()

# File command mapping
doc_map = {
    "ml unit 1 pdf": r"C:\Users\User\Documents\ML_Unit1.pdf"
}

def match_file(cmd):
    best = difflib.get_close_matches(cmd.lower(), doc_map.keys(), n=1, cutoff=0.5)
    if best:
        os.startfile(doc_map[best[0]])

# Detect letter (basic P shape)
def detect_letter_p(landmarks):
    return landmarks[8].x < landmarks[6].x and landmarks[12].y < landmarks[10].y

# Camera setup
cap = cv2.VideoCapture(0)
last_action = ''
cursor_enabled = False

def process_voice():
    data = stream.read(4000, exception_on_overflow=False)
    if recognizer.AcceptWaveform(data):
        result = json.loads(recognizer.Result())
        cmd = result['text']
        print("You said:", cmd)

        if "close all tab" in cmd:
            pyautogui.hotkey('ctrl', 'shift', 'w')
        elif "move cursor" in cmd:
            global cursor_enabled
            cursor_enabled = True
        elif "stop cursor" in cmd:
            cursor_enabled = False
        elif "open powerpoint" in cmd:
            os.system("start POWERPNT.EXE")
        elif "open files" in cmd:
            match_file(cmd)
        elif "stop" in cmd:
            speak("Stopping detection")
            return False
    return True

while True:
    if not process_voice():
        break

    ret, frame = cap.read()
    if not ret:
        break

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(frame_rgb)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            lm = hand_landmarks.landmark

            # Fist gesture
            if all(lm[i].y > lm[0].y for i in [4, 8, 12, 16, 20]):
                if last_action != 'fist':
                    speak("Fist detected - Opening Notepad")
                    os.system("start notepad")
                    last_action = 'fist'

            # Index finger gesture
            elif lm[8].y < lm[6].y and all(lm[i].y > lm[0].y for i in [4, 12, 16, 20]):
                if last_action != 'index':
                    speak("Index detected - Opening Camera")
                    os.system("start microsoft.windows.camera:")
                    last_action = 'index'

            # Letter P gesture
            elif detect_letter_p(lm):
                if last_action != 'P':
                    speak("P gesture - Opening PowerPoint")
                    os.system("start POWERPNT.EXE")
                    last_action = 'P'

            # Cursor control
            elif cursor_enabled:
                x = int(lm[8].x * pyautogui.size()[0])
                y = int(lm[8].y * pyautogui.size()[1])
                pyautogui.moveTo(x, y)

    cv2.imshow("Gesture + Voice Control", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
stream.stop_stream()
stream.close()
mic.terminate()