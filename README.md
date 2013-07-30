btsync_status
=============

Command line python script for monitoring your BitTorrent Sync server status.

## What
This python script uses the webui for btsync to output the sync status of folders to a terminal.

## How

    $ ./btsync_status.py [config_file]

    /home/ds/photos: 151.5 GB in 81416 files
      bup:  ↑ 835 B
    /home/ds/testing: 1.9 GB in 4 files
      bup: ↓ 7.4 GB
    /home/ds/test: 172.6 MB in 15 files
      phone:  Synced on 07/30/13 15:51:45
    /home/ds/tunes: 9.9 GB in 1417 files
      phone: ↓ 21.8 GB
    1.4 kB/s up, 2.7 MB/s down

## Configuration

Example configuration is in the config.json.example file.

    username: if using http auth. optional.
    password: if using http auth. optional.
    host: host of btsync server. optiona. defaults to localhost.
    port: port of webui. optional. defaults to 8888.
    proto: proto for webui. http/https. optional. defaults to http.
    sleep_interval: time to sleep before refreshing status from btsync. optional. defaults to 5 seconds

##