import sounddevice as sd
import wavio
import datetime
import os
import logging
import concurrent.futures
import time

freq = 44100
duration = 4  # in seconds
recordings_dir = './recordings'  # Create the recordings directory if it doesn't exist
logging.basicConfig(level=logging.DEBUG, filename='recorder_log.txt')


def record_audio():
    start = time.perf_counter()
    if not os.path.exists(recordings_dir):
        os.makedirs(recordings_dir)
    print('Recording')
    ts = datetime.datetime.now()  # create a timestamp to assign to audio files as they're made
    filename = ts.strftime("%H:%M:%S")  # Start recorder with the given values of duration and sample frequency
    logging.debug('recording started @:' + filename)
    recording = sd.rec(int(duration * freq), samplerate=freq,
                       channels=1)  # Record audio for the given number of seconds
    sd.wait()  # wait for recording to end before writing file
    end_ts = datetime.datetime.now()
    logging.debug('recording ended @' + end_ts.strftime('%H:%M:%S'))
    file = (recording, filename)
    end = time.perf_counter()
    runtime = end - start
    logging.info('recording loop ran: ' + str(runtime))
    return file


def write_wav_file(file):
    wavio.write(f'{recordings_dir}/{file[1]}.wav', file[0], freq, sampwidth=2, clip='ignore')


while True:
    with concurrent.futures.ThreadPoolExecutor() as ex:
        rec_proc = ex.submit(record_audio)
        result = rec_proc.result()
        file_write_proc = ex.submit(write_wav_file, result)
