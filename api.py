#!/usr/bin/python3

from flask import Flask
from flask_cors import CORS
from src.config import config
from src.qbittorrent import torrents

api = Flask(__name__)
api.register_blueprint(torrents)

if __name__ == "__main__":
    api.run(host=config.APPHOST, port=config.APPPORT)