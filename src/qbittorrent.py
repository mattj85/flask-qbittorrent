#!/usr/bin/python3

from qbittorrent import Client
from flask import Flask, json, jsonify, request, make_response, Blueprint
from flask_cors import CORS

# config
from .config import config

# register blueprint
torrents = Blueprint('torrents', __name__)
CORS(torrents)

# init torrent connection - localhost
qb = Client("http://{}:{}".format(config.QBITAPIHOST, config.QBITAPIPORT))
qb.login(config.QBITUSERNAME, config.QBITPASSWORD)


#
# torrent info
#
@torrents.route('/api/qbt/list', methods=["GET"])
def listTorrents():
    try:
        torrents = qb.torrents()
        activeTorrents = []
        for torrent in torrents:
            torrentHash = torrent["hash"]
            torrentName = torrent["name"]
            torrentTotalSize = torrent["total_size"]
            torrentDownloaded = torrent["completed"]

            # default vars
            torrentStatus = "active"
            torrentCompleted = False
            torrentPercentage = 0

            # downlaod finished?
            if torrentDownloaded == torrentTotalSize:
                torrentCompleted = True
                torrentPercentage = "100.00"
                torrentStatus = "complete"

            # if active, calculate rough download %
            if torrentCompleted == False:
                torrentPercentage = "{:.2f}".format(torrentDownloaded * 100 / torrentTotalSize)

            # get torrent state
            if torrent["state"] == "pausedDL":
                torrentStatus = "paused"
            elif torrent["state"] == "stalledUP":
                torrentStatus = "complete"

            # get torrent path
            torrentPath = "{}{}{}".format(config.QBITDOWNLOADPATH, torrent["save_path"], torrent["name"])

            # build return object
            torrentObject = {"torrent_name": torrentName, "torrent_hash": torrentHash, "torrent_size": torrentTotalSize, "torrent_downloaded": torrentDownloaded, "torrent_completed": torrentCompleted, "torrent_percentage": torrentPercentage, "torrent_status": torrentStatus, "torrent_path": torrentPath }
            activeTorrents.append(torrentObject)
        
        response = make_response(
            jsonify(
                    {
                        "status_code": 200,
                        "torrents": activeTorrents
                    }
                ),
                200,
            )
        return response
    except Exception as e:
        response = make_response(
        jsonify(
                {
                    "status_code": 500,
                    "message": "Error: " + str(e)
                }
            ),
            500,
        )
        return response

#
# add torrent
#
@torrents.route('/api/qbt/add', methods=['POST'])
def addMagnetLink():
    try:
        req = request.json
        magnetLink = req["magnet"]
        qb.download_from_link(magnetLink)
        response = make_response(
        jsonify(
                {
                    "status_code": 200,
                    "message": "torrent added"
                }
            ),
            200,
        )
        return response
    except Exception as e:
        response = make_response(
        jsonify(
                {
                    "status_code": 500,
                    "message": str(e)
                }
            ),
            500,
        )
        return response

#
# torrent control
#
@torrents.route('/api/qbt/pause', methods=["POST"])
def pauseTorrent():
    try:
        req = request.json
        torrentHash = req["hash"]

        pauseAll = False
        if torrentHash == "all":
            qb.pause_all()
            pauseAll = True
            message = "all torrents paused"

        if not pauseAll:
            qb.pause(torrentHash)
            message = "torrent paused"
        
        response = make_response(
        jsonify(
                {
                    "status_code": 200,
                    "message": message
                }
            ),
            200,
        )
        return response
        
    except Exception as e:
        response = make_response(
        jsonify(
                {
                    "status_code": 500,
                    "message": str(e)
                }
            ),
            500,
        )
        return response

@torrents.route('/api/qbt/resume', methods=["POST"])
def resumeTorrent():
    try:
        req = request.json
        torrentHash = req["hash"]

        resumeAll = False
        if torrentHash == "all":
            qb.resume_all()
            resumeAll = True
            message = "all torrents resumed"

        if not resumeAll:
            qb.resume(torrentHash)
            message = "torrent resumed"
        
        response = make_response(
        jsonify(
                {
                    "status_code": 200,
                    "message": message
                }
            ),
            200,
        )
        return response
        
    except Exception as e:
        response = make_response(
        jsonify(
                {
                    "status_code": 500,
                    "message": str(e)
                }
            ),
            500,
        )
        return response

@torrents.route('/api/qbt/delete', methods=["POST"])
def deleteTorrent():
    try:
        req = request.json
        torrentHash = req["hash"]

        deleteAll = False
        if torrentHash == "all":
            qb.delete_all()
            deleteAll = True
            message = "all torrents deleted"

        if not deleteAll:
            qb.delete(torrentHash)
            message = "torrent deleted"
        
        response = make_response(
        jsonify(
                {
                    "status_code": 200,
                    "message": message
                }
            ),
            200,
        )
        return response
        
    except Exception as e:
        response = make_response(
        jsonify(
                {
                    "status_code": 500,
                    "message": str(e)
                }
            ),
            500,
        )
        return response