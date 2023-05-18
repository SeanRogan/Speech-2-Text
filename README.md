# speech2text
### An experiment created to attempt near-real-time voice transcription via the openai whisper model. 

currently the best way to run the prototype is to run recorder.py and scribe.py as separate processes in two terminal windows,
and the transcripts will be printed to the console. Future versions will work by running the main script.

## Requirements:

We are using the openai API for transcription. You will need an openai API key stored in a file called constants.py,
in the same home directory where recorder.py and scribe.py are located. example:
```
OPENAI_API_KEY = 'sk-ztiVKBxadjskjlkasjkldj238108154dsfsafsadf768iZPDc5O'
```

### Concurrency_ versions

There is a concurrency_recorder script and a concurrency_scribe script, which use multithreading in the hopes of getting better performance. The concurrent_recorder works, but does not seem to work any faster than the single threaded version. We recommend running the single threaded version. The concurrency_scribe spawns a new thread to call the API and then append the result to the transcript file. This seems to improve the speed over the single threaded version by nearly 100% in my limited testing. I recommend the use of the concurrent_scribe.py script over the single threaded scribe.py script. Run the two scripts separately from the terminal in different shells.