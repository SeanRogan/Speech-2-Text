import sounddevice as sd
import wavio
import datetime
import os
import logging
import concurrent.futures
import time
import argparse

logging.basicConfig(level=logging.DEBUG, filename='recorder_log.txt')
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


def record_audio():
    start = time.perf_counter()
    if not os.path.exists(recordings_dir):
        os.makedirs(recordings_dir)  # Create the recordings directory if it doesn't exist
    print('Recording')
    ts = datetime.datetime.now()  # create a timestamp to assign to audio files as they're made
    filename = ts.strftime("%H:%M:%S")  # Start recorder with the given values of duration and sample frequency
    logging.debug('recording started @:' + filename)
    recording = sd.rec(int(duration * freq), samplerate=freq,
                       channels=1)  # Record audio for the given number of seconds
    sd.wait()  # wait for recording to end before writing file
    end_ts = datetime.datetime.now()
    logging.debug('recording ended @' + end_ts.strftime('%H:%M:%S'))
    file = (recording, filename)  # create a tuple with the recording data and file name to be returned
    end = time.perf_counter()  # perf test logging timer
    runtime = end - start
    logging.info('recording loop runtime: ' + str(runtime))
    return file


def write_wav_file(file):
    start = time.perf_counter()
    wavio.write(f'{recordings_dir}/{file[1]}.wav', file[0], freq, sampwidth=2, clip='ignore')   # write wav data to file
    end = time.perf_counter()  # perf test logging timer
    runtime = end - start
    logging.info('file write loop runtime: ' + str(runtime))


while True:
    with concurrent.futures.ThreadPoolExecutor() as ex:
        rec_proc = ex.submit(record_audio)
        result = rec_proc.result()
        file_write_proc = ex.submit(write_wav_file, result)
