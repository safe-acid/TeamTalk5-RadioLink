# TeamTalk5-RadioLink
This is a simple radio player for TeamTalk5 with predefined radio stations. Use your own stations as you wish. The bot will reconnect automatically if the server is rebooted.

### Minimum requirements:
* Windows 10/11       x64
* Mac OS X (10.9)     x86_64
* Linux (Ubuntu 22)   x86_64
* Python 3.11 or later

# Installation 

## 1. Install Requirements
Install python requirements from requirements.txt
```shell script
pip install -r requirements.txt
```
Download essentiial TeamTalk5 SDK using the command
```shell script
python setup.py
```
Windows users must install a <a href = "https://www.videolan.org/vlc/download-windows.html">VLC player</a>
Linux 
```shell script
sudo apt install vlc
sudo apt install ffmpeg
```
Mac
```shell script
brew install vlc
brew install ffmpeg
```
## 2. Set Up Audio Device ID
Define Audio Device ID by running the command
```shell script
python radio.py --devices
```

## 3. Configure Settings
Update your Audio ID and server's settings in config.py file

## 4. Run the Bot
Run the RadioLink by command
```shell script
python radio.py
```

The default langauge is English, if you want to run on Russian use command
```shell script
python radio.py --language ru
```

### Release notes version:
1.0 - initial release

1.1 - added ffmpeg player

Telegram - <a href="https://t.me/TT5RadioLink"> TT5RadioLink</a>

Good Luck:
Котяра 🐾


