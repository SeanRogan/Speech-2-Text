import sounddevice as sd
import wavio
import datetime
import os


freq = 44100
duration = 5  # in seconds
recordings_dir = './recordings'  # Create the recordings directory if it doesn't exist
if not os.path.exists(recordings_dir):
    os.makedirs(recordings_dir)
print('Recording')
while True:
    ts = datetime.datetime.now()    # create a timestamp to assign to audio files as they're made

    filename = ts.strftime("%H:%M:%S")  # Start recorder with the given values of duration and sample frequency
    recording = sd.rec(int(duration * freq), samplerate=freq, channels=1)  # Record audio for the given number of seconds
    sd.wait()
    wavio.write(f"./recordings/{filename}.wav", recording, freq, sampwidth=2, clip="ignore")  # Convert the NumPy array to audio file

