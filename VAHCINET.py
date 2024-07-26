import os
import pyaudio
import numpy as np
import subprocess
import tempfile
import time
import wave
import re
import webbrowser
import speech_recognition as sr
import pyautogui

# Record Audio using PyAudio with Countdown
def record_audio(duration, fs):
    # Countdown before recording
    countdown_time = 3
    while countdown_time > 0:
        print(f"Starting recording in {countdown_time} seconds...")
        time.sleep(1)
        countdown_time -= 1

    print(f"Recording audio for {duration} seconds...")

    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=fs,
                    input=True,
                    frames_per_buffer=int(fs/10))  # Adjust frames_per_buffer as needed

    frames = []

    for i in range(0, int(fs / int(fs/10) * duration)):
        data = stream.read(int(fs/10))
        frames.append(data)

    stream.stop_stream()
    stream.close()
    p.terminate()

    audio_data = np.frombuffer(b''.join(frames), dtype=np.int16)

    return audio_data

# Function to extract features from audio
def extract_features(myrecording, fs, expected_features=64000):
    window_size = 5000  # milliseconds
    n_frames = int(window_size * fs / 1000)

    # Trim the recording to exactly 32000 samples
    myrecording = myrecording[:64000]

    # Compute the raw features (for example, use the flattened audio signal)
    raw_features = myrecording.flatten()

    # Ensure the feature vector has the expected size
    if len(raw_features) < expected_features:
        # If the features are less than expected, pad with zeros
        raw_features = np.pad(raw_features, (0, expected_features - len(raw_features)))

    return raw_features[:expected_features]

# Function to write features to text file
def write_to_text_file(features, filename='features.txt'):
    # Get the current working directory
    current_directory = os.getcwd()

    # Create the full path for the file in the current directory
    file_path = os.path.join(current_directory, filename)

    with open(file_path, 'w') as file:
        feature_str = ','.join(map(str, features))
        file.write(feature_str)

# Function to clear contents of text file
def clear_text_file(filename='features.txt'):
    # Get the current working directory
    current_directory = os.getcwd()

    # Create the full path for the file in the current directory
    file_path = os.path.join(current_directory, filename)

    # Clear the contents of the file
    with open(file_path, 'w') as file:
        file.write('')

# Function to write classification result to text file
def write_classification_result(result, filename='VisualPrediction.txt'):
    # Get the current working directory
    current_directory = os.getcwd()

    # Create the full path for the file in the current directory
    file_path = os.path.join(current_directory, filename)

    with open(file_path, 'w') as file:
        file.write(result)

# Function to classify features
def classify_features(raw_features):
    # Write features to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, mode='w') as temp:
        # Write raw features directly to the temporary file
        temp.write(','.join(map(str, raw_features)))
    try:
        # Call Node.js process and pass filename
        result = subprocess.check_output(['node', 'run-impulse.js', temp.name])
        result = result.decode('utf-8').strip()
        if result:
            return result
        else:
            print("Classification result is empty.")
            return None
    except subprocess.CalledProcessError as e:
        print(f"Failed to initialize classifier. Error: {e}")
        return None

# Function to save audio as WAV file
def save_as_wav(audio_data, filename='recording.wav', sample_rate=16000):
    file_path = os.path.join(os.getcwd(), filename)
    with wave.open(file_path, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(audio_data.tobytes())

def open_youtube_and_search(query):
    search_url = f"https://www.youtube.com/results?search_query={query}"
    webbrowser.open(search_url)
    print(f"Opened YouTube and searched for '{query}'.")

# For the 35 Class Shutdown Computer
def update_visual_prediction_labels(filename='VisualPrediction.txt'):
    # Get the current working directory
    current_directory = os.getcwd()

    # Create the full path for the file in the current directory
    file_path = os.path.join(current_directory, filename)

    try:
        with open(file_path, 'r') as file:
            content = file.read()
            # Parse the classification result to find the label with the highest value
            labels_and_values = re.findall(r"label: '([^']*)', value: ([\d.]+)", content)
            max_label, max_value = max(labels_and_values, key=lambda x: float(x[1]))

            actions = {
                "Exit Calculator": "calculatorapp.exe",
                "Exit Calendar": "HxCalendarAppImm.exe",
                "Exit Camera": "WindowsCamera.exe",
                "Exit File Manager": "explorer0.exe",
                "Exit Microsoft Excel": "EXCEL.exe",
                "Exit Microsoft Powerpoint": "POWERPNT.exe",
                "Exit Microsoft Word": "WINWORD.exe",
                "Exit Notepad": "notepad.exe",
                "Exit Paint": "mspaint.exe",
                "Exit Sticky Notes": "Microsoft.Notes.exe",
                "Exit Voice Recorder": "SoundRec.exe",
                "Exit Zoom App": "Zoom.exe",

                # Add actions to open applications
                "Open Calculator": "calc.exe",
                "Open Calendar": "start outlookcal:",
                "Open Camera": "start microsoft.windows.camera:",
                "Open File Manager": "explorer.exe",
                "Open Microsoft Excel": "start excel.exe",
                "Open Powerpoint": "start POWERPNT.exe",
                "Open Microsoft Word": "start winword.exe",
                "Open Notepad": "notepad.exe",
                "Open Paint": "mspaint.exe",
                "Open Sticky Notes": "start shell:AppsFolder\Microsoft.MicrosoftStickyNotes_8wekyb3d8bbwe!App",
                "Open Voice Recorder": "start shell:AppsFolder\Microsoft.WindowsSoundRecorder_8wekyb3d8bbwe!App",
                "Open Zoom App": "start zoommtg:",
                "Open Browser and search": "browser_search",
                "Open File": "explorer shell:Documents",
                "Open Google": "webbrowser.open('https://www.google.com')",
                "Open youtube and search": "youtube_search",
                "Open Folder": "explorer shell:Downloads",
                "Open google and search": "open_google_and_search",
                "Print": "print_file",
                "Save File": "save_file",
            }

            print(f"Max label: {max_label}")

            if max_label == "Print":
                # Simulate pressing Ctrl+P
                pyautogui.hotkey('ctrl', 'p')
                print("Ctrl+P simulated for printing")
            elif max_label == "Save File":
                # Simulate pressing Ctrl + S
                pyautogui.hotkey('ctrl', 's')
                print("Ctrl+S simulated for saving")
            else:
                print(f"Executed {max_label}.")

            if max_label == "Open google and search":
                # Load the WAV file
                audio_file = os.path.join(current_directory, "recorded_audio.wav")

                # Use the recognizer to convert audio to text
                recognizer = sr.Recognizer()
                with sr.AudioFile(audio_file) as source:
                    audio = recognizer.record(source)

                try:
                    query = recognizer.recognize_google(audio)
                    print(f"Full command: {query}")
                    # Extract the query from the command
                    query = query.split("search")[-1].strip()
                    print(f"Search query: {query}")
                    if query:
                        search_url = f"https://www.google.com/search?q={query}"
                        webbrowser.open(search_url)
                        print(f"Opened Google and searched for '{query}'.")
                    else:
                        print("No search query provided.")
                except sr.UnknownValueError:
                    print("Could not understand audio.")
                except sr.RequestError as e:
                    print(f"Could not request results; {e}")
            else:
                print(f"Executed {max_label}.")

            if max_label.lower() == "open youtube and search":
                # Load the WAV file
                audio_file = os.path.join(current_directory, "recorded_audio.wav")

                # Use the recognizer to convert audio to text
                recognizer = sr.Recognizer()
                with sr.AudioFile(audio_file) as source:
                    audio = recognizer.record(source)

                try:
                    query = recognizer.recognize_google(audio)
                    print(f"Full command: {query}")
                    # Extract the query from the command
                    query = query.split("search")[-1].strip()
                    print(f"Search query: {query}")
                    if query:
                        search_url = f"https://www.youtube.com/results?search_query={query}"
                        webbrowser.open(search_url)
                        print(f"Opened youtube and searched for '{query}'.")


                    else:
                        print("No search query provided.")
                except sr.UnknownValueError:
                    print("Could not understand audio.")
                except sr.RequestError as e:
                    print(f"Could not request results; {e}")
            else:
                print(f"Executed {max_label}.")

            if max_label == "Open Browser and search":
                # Load the WAV file
                audio_file = os.path.join(current_directory, "recorded_audio.wav")

                # Use the recognizer to convert audio to text
                recognizer = sr.Recognizer()
                with sr.AudioFile(audio_file) as source:
                    audio = recognizer.record(source)

                try:
                    query = recognizer.recognize_google(audio)
                    print(f"Full command: {query}")
                    # Extract the query from the command
                    query = query.split("search")[-1].strip()
                    print(f"Search query: {query}")
                    if query:
                        search_url = f"https://www.google.com/search?q={query}"
                        webbrowser.open(search_url)
                        print(f"Opened browser and searched for '{query}'.")
                    else:
                        print("No search query provided.")
                except sr.UnknownValueError:
                    print("Could not understand audio.")
                except sr.RequestError as e:
                    print(f"Could not request results; {e}")
            else:
                print(f"Executed {max_label}.")

                if max_label.startswith("Open"):
                    subprocess.Popen(actions[max_label], shell=True)
                    print(f"{max_label} executed.")
                else:
                    app_name = actions[max_label]
                    result = subprocess.run(["taskkill", "/IM", app_name, "/F"], capture_output=True, text=True)
                    if result.returncode == 0:
                        print(f"{max_label} executed.")
                    else:
                        print(f"Failed to Execute {max_label} app: {result.stderr}")
            if max_label == "Exit Google":
                subprocess.Popen(["taskkill", "/IM", "chrome.exe", "/FI", "WINDOWTITLE eq Google - Google Chrome"],
                                 shell=True)
                print("Google tab closed.")
            else:
                print(
                    f"The label with the highest value '{max_label}' does not match any predefined action. No changes made.")

            if max_label == "Open Google":
                webbrowser.open('https://www.google.com')
                print("Opened Google in the default browser.")

    except FileNotFoundError:
        print("VisualPrediction.txt not found.")

# Main Function
def main():
    duration = 5  # seconds
    fs = 16000
    expected_features = 64000  # Adjust based on your requirements
    myrecording = record_audio(duration, fs)

    # Save the recorded audio as a WAV file
    save_as_wav(myrecording, filename='recorded_audio.wav')

    # Calculate the number of extracted features
    raw_features = extract_features(myrecording, fs, expected_features)
    num_extracted_features = len(raw_features)
    print(f"Number of extracted features: {num_extracted_features}")

    # Write features to a text file in the same directory
    write_to_text_file(raw_features, filename='features.txt')

    try:
        result = classify_features(raw_features)
        if result is not None:
            print('Classification Result:', result)
            # Write classification result to VisualPrediction.txt
            write_classification_result(result, filename='VisualPrediction.txt')
        else:
            print('No classification result')
    except Exception as e:
        print(f"Exception during classification: {e}")
    finally:
        # Clear contents of features.txt after program exits
        clear_text_file()
        # Update VisualPrediction.txt labels
        update_visual_prediction_labels()

if __name__ == "__main__":
    main()
