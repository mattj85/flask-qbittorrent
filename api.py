#!/usr/bin/python3

from flask import Flask
from src.qbittorrent import torrents

torrentApi = Flask(__name__)

torrentApi.register_blueprint(torrents)

if __name__ == "__main__":
    torrentApi.run(host="0.0.0.0", port=5000)