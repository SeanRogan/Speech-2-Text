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
