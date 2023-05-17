import datetime
import logging
import tempfile
import wavio
import openai
import constants
import multiprocessing as mp
import sounddevice as sd
import concurrent.futures
import scribe as s
import recorder as r
import os
import glob
import time

logging.basicConfig(level=logging.DEBUG, filename='log.txt')
last_processed_time = 0  # last processed file timestamp
transcribed = []  # list to hold files already transcribed to avoid duplicate api calls


def record(freq=44100, duration=5):
    recordings_dir = './recordings'  # Create the recordings directory if it doesn't exist
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
    wavio.write(f"./recordings/{filename}.wav", recording, freq, sampwidth=2,
                clip="ignore")  # Convert the NumPy array to audio file


def transcribe(freq=44100):
    global last_processed_time
    start = datetime.datetime.now()
    files = glob.glob("./recordings/*")  # files are in the recordings dir
    unprocessed_files = [f for f in files if os.path.getctime(
        f) > last_processed_time]  # unprocessed_files are any with a timestamp more recent than the last_processed_file's timestamp
    if not unprocessed_files:
        time.sleep(1)  # if there aren't any files to process, sleep 1second and restart loop
        pass

    latest = max(unprocessed_files,
                 key=os.path.getctime)  # sort unprocessed files by timestamp to find latest recording

    logging.debug(str(latest))
    latest_filename = latest.split('/')[2]  # split file id from dir id
    logging.debug("latest filename is : " + str(latest_filename))

    if latest not in transcribed and os.path.exists(
            latest):  # if file path exists and is not present in the 'transcribed' list of files already processed..
        with open(latest, 'rb') as file:  # open file..
            logging.debug('calling api with file: ' + str(latest))
            result = openai.Audio.transcribe("whisper-1", file,
                                             api_key=constants.OPENAI_API_KEY)  # OpenAI API call, args include whisper model, sending the file object,and the api key
        logging.debug("api call success")
        print(str(result.text))  # print the results of the api call

        # todo handler service to deal with results of api call

        # record end-time time stamp, prints api call delay time for testing/eval
        end = datetime.datetime.now()
        runtime = end - start
        logging.debug('runtime for scribe loop was : ' + str(runtime))
        # append text to transcript file
        trans_ts_start = datetime.datetime.now()
        with open('transcription.txt', 'a') as f:
            f.write(result.text)
        transcribed.append(latest)
        trans_ts_end = datetime.datetime.now()
        transcribed_time = trans_ts_end - trans_ts_start
        logging.debug('transcription took :' + str(transcribed_time))
        # save list of transcribed recordings so that we don't transcribe the same one again
        last_processed_time = os.path.getctime(latest)  # record file timestamp as new last_processed_file


if __name__ == '__main__':
    # this single process style prototype works, but it is far too slow, it takes 8 seconds to complete the loop.
    # running the scribe and recorder scripts as two separate processes only takes 4sec to complete the loop
    # openai API call averages near 750-900ms to respond.

    r_proc = mp.Process(target=r.rec)
    s_proc = mp.Process(target=s.scribe)
    r_proc.start()
    s_proc.start()
    r_proc.join()
    s_proc.join()

