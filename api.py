#!/usr/bin/python3

from flask import Flask, request
from flask_cors import CORS
from src.config import config
from src.qbittorrent import torrents

api = Flask(__name__, static_url_path="/static")
api.register_blueprint(torrents)

# service dashboard
@api.route('/')
def root():
    return api.send_static_file('index.html')

if __name__ == "__main__":
    api.run(host=config.APPHOST, port=config.APPPORT)