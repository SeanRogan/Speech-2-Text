import sounddevice as sd
import wavio
import datetime
import os
import logging
import time
import argparse

logging.basicConfig(level=logging.DEBUG, filename='log.txt')

parser = argparse.ArgumentParser()
parser.add_argument('-d', '--Directory', type=str, required=False, help='Configure the directory to which recordings are saved. Takes a string representing the file path where audio files are to be saved.')
parser.add_argument('-s', '--Seconds', type=int, required =False, help='Configure the recording time, in seconds. Takes an integer, representing the length of recording interval. An argument of 7 will record a series of wav files 7 seconds long, until the script is stopped. Default setting is 5 seconds.')
args = parser.parse_args()
freq = 44100
duration = 5  # recording duration, in seconds
if args.Seconds is not None:
    duration = args.Seconds
recordings_dir = './recordings'
if args.Directory is not None:
    recordings_dir = args.Directory

if not os.path.exists(recordings_dir):
    os.makedirs(recordings_dir)  # Create the recordings directory if it doesn't exist

print('Recording')
while True:
    start = time.perf_counter()
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
    end = time.perf_counter()
    rt = str(end - start)
    logging.info(f'recording loop runtime for {duration}s: {rt}')
