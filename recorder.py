import sounddevice as sd
import wavio
import datetime
import os
import logging

freq = 44100
duration = 4  # in seconds
recordings_dir = './recordings'  # Create the recordings directory if it doesn't exist
logging.basicConfig(level=logging.DEBUG, filename='log.txt')


if not os.path.exists(recordings_dir):
    os.makedirs(recordings_dir)
print('Recording')
while True:
    ts = datetime.datetime.now()  # create a timestamp to assign to audio files as they're made
    filename = ts.strftime("%H:%M:%S")  # Start recorder with the given values of duration and sample frequency
    logging.debug('recording started @:' + filename)
    recording = sd.rec(int(duration * freq), samplerate=freq,
                       channels=1)  # Record audio for the given number of seconds
    sd.wait()  # wait for recording to end before writing file
    end_ts = datetime.datetime.now()
    logging.debug('recording ended @' + end_ts.strftime('%H:%M:%S'))
    wavio.write(f"./recordings/{filename}.wav", recording, freq, sampwidth=2,
                clip="ignore")  # Convert the NumPy array to audio file
