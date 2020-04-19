# Delta-Bot
Delta here is my magnet tracker. Using a python module called [bs4](https://pypi.org/project/beautifulsoup4/) it scrapes 1337x.to based on a particular encoder or a search query. It also selectively skips dead and already leeched torrents. Messages are timed algorithmically to 3 different groups to escape the floodlimit on bots by Telegram. 

The common code for my torrent leechers on Telegram namely Alpha, Beta and Gamma can be found [here](https://github.com/Syzygianinfern0/Alpha-Bot). Using `aria2c` for the leeching and python for the chat interface and uploading to my Drive, each bot can leech upto 20 torrents/DDLs at a time at a max speed of 50MBps, hence would tingle the datahoarder in anyone.  

As communication prohibited between bots (by Telegram), I came up with a workaround named [BoTransmission](https://github.com/Syzygianinfern0/BoTransmission) for relaying messages between the bots. Basically the configuration in practice is, Alpha, Beta and Gamma are in a group and Delta in 3 other groups (workaround for flood limit of bots). BoTransmission takes control of my personal account and forwards messages from the scraping groups (from Delta) to the leech group hence working around the communication with my account being the medium. 

[Contact me on telegram](https://t.me/Syzygianinfern0) to gain access to these jewls.