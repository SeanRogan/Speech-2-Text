import glob
import os
import datetime
import time
import openai
import constants
import logging


def scribe():
    start = datetime.datetime.now()
    last_processed_time = 0
    transcribed = []

    while True:
        files = glob.glob("./recordings/*")
        unprocessed_files = [f for f in files if os.path.getctime(f) > last_processed_time]
        if not unprocessed_files:
            time.sleep(1)
            continue

        latest = max(unprocessed_files, key=os.path.getctime)
        last_processed_time = os.path.getctime(latest)

        logging.debug(str(latest))
        latest_filename = latest.split('/')[1]  # split file id from dir id
        logging.debug("latest filename is : " + str(latest_filename))

        if os.path.exists(
                latest) and not latest in transcribed:  # if file path exists and is not present in the 'transcribed' list of files already processed..
            with open(latest, 'rb') as file:  # open file..
                result = openai.Audio.transcribe("whisper-1", file,
                                                 api_key=constants.OPENAI_API_KEY)  # OpenAI API call, args include whisper model, sending the file object,and the api key
            logging.debug("api call success")
            print(str(result.text))  # print the results of the api call

            # todo handler service to deal with results of api call

            # record end-time time stamp, prints api call delay time for testing/eval
            end = datetime.datetime.now()
            runtime = end - start
            print(runtime)

            # append text to transcript file
            with open('transcription.txt', 'a') as f:
                f.write(result.text)
            # save list of transcribed recordings so that we don't transcribe the same one again
            transcribed.append(latest)
            time.sleep(.5)
