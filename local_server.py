from flask import Flask, request
from playsound3 import playsound

app = Flask(__name__)

@app.route("/play/<folder_name>")
def play_sounds(folder_name: str):
    file_name=request.args.get("filename")
    playsound(f"{folder_name}/{file_name}.m4a")
    return "sound was played"

