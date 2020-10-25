#!/usr/bin/python3

from flask import Flask
from src.config import config
from src.qbittorrent import torrents

torrentApi = Flask(__name__)

torrentApi.register_blueprint(torrents)

if __name__ == "__main__":
    torrentApi.run(host=config.APPHOST, port=config.APPPORT)