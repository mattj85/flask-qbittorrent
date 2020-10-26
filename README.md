# flask-qbittorrent

This is a flask wrapper for the python-qbittorrent module. The project came from the need of access to the qbittorrent-nox on an iPhone. The regular site is not responsive on a iOS device. Simple bootstrap front end to allow control of active torrents and the ability to start a new download via magnet link or torrent file.

### Functions
* Overview of current downloads
* Add torrent via magnet link or file
* Start / pause / delete torrents
* Basic notifications

Project runs on port 5000 and the overview page is served as the web root. Designed to be run on home LAN, no authentication currently (only to the qbittorrent API)
