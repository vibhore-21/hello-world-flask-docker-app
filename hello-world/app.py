#!/usr/bin/python
import os
import time
import socket
from flask import Flask


app = Flask(__name__)

START = time.time()
PORT = os.getenv("PORT", 4002)
HOST = os.getenv("HOST", '0.0.0.0')
DEBUG = bool(os.getenv("DEBUG"))


def elapsed():
    running = time.time() - START
    minutes, seconds = divmod(running, 60)
    hours, minutes = divmod(minutes, 60)
    return "%d:%02d:%02d" % (hours, minutes, seconds)


@app.route('/')
def root():
    return "[HOST:%s] Hello World!!! (Server up time: %s) \n" % (socket.gethostname(), elapsed())


if __name__ == "__main__":
    app.run(debug=DEBUG,
            host=HOST,
            port=int(PORT))
