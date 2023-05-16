import datetime
import logging
import tempfile
import wavio
import openai
import constants
import multiprocessing as mp
import sounddevice as sd
import concurrent.futures
from io import BytesIO

logging.basicConfig(level=logging.DEBUG)


def record(q, freq=44100, duration=5):
    while True:
        increment = 0
        # create a timestamp to assign to audio files as they're made
        ts = datetime.datetime.now()
        filename = ts.strftime("%H:%M:%S")  # Start recorder with the given values of duration and sample frequency
        recording = sd.rec(int(duration * freq), samplerate=freq,
                           channels=1)  # Record audio for the given number of seconds
        sd.wait()  # wait for recording to end
        q.put((filename, recording))
        logging.debug(f"file : {filename} appended to queue ")
        increment += 1
        logging.debug(increment)
        # wavio.write(f"{filename}.wav", recording, freq, sampwidth=2, clip="ignore")


def transcribe(q, freq=44100):
    while True:
        increment = 0

        transcribed = []
        start = datetime.datetime.now()
        result, filename = ""
        if not q.empty():
            filename, wav_data = q.get()
            file = wavio.write(f"./recordings/{filename}.wav", wav_data, freq, sampwidth=2, clip="ignore")
            startcall = datetime.datetime.now()
            result = openai.Audio.transcribe("whisper-1", file,
                                             api_key=constants.OPENAI_API_KEY)  # OpenAI API call, args include whisper model, sending the file object,and the api key
            endcall = datetime.datetime.now()
            api_call_time = endcall - startcall
            logging.debug("api call success. delay :  " + api_call_time)
            print(str(result.text))  # print the results of the api call
        end = datetime.datetime.now()
        runtime = end - start
        print(runtime)
        try:
            with open('transcription.txt', 'a') as f:
                f.write(result.text)
            transcribed.append(filename)
        except AttributeError as ae:
            logging.warning(str(ae))
            print('an error occurred while transcribing to the text file')
    #  # Convert the NumPy array to audio file


if __name__ == '__main__':

    # queue = mp.Queue()
    # while True:
    #     with concurrent.futures.ProcessPoolExecutor() as executor:
    #         future1 = executor.submit(record, queue)
    #         future2 = executor.submit(transcribe, queue)
