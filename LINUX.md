# Installation from zero on Linux Ubuntu 22+/Debian 12+

```shell script
sudo apt update
```
### check in python is installed
```shell script
python3 —version 
```
### install python if need it
```shell script
sudo apt install python3
```
### check if pip installed
```shell script
pip — version
```
### instal pip if need it
```shell script
python3 -m pip install --upgrade pip 
```
### install git
```shell script
sudo apt install git
```
### install pulse audio, vlc, ffmpeg
```shell script
sudo apt install pulseaudio
sudo apt install vlc
sudo apt install ffmpeg
```
### verify 
```shell script
pulseaudio --version
vlc --version
ffmpeg --version
```
### start pulseaudio
```shell script
pulseaudio —start
```
### add Virtual audio devices
```shell script
pactl load-module module-null-sink sink_name=Source
pactl load-module module-virtual-source source_name=VirtualMic master=Source.monitor
```
### after steps above you shoud get number IDss after creating null-sinks, it means all goes well,create config file
```shell script
nano ~/.config/pulse/default.pa 
```
### add configuratioon into default.pa and save the file 
```shell script
# include the default.pa pulseaudio config file
.include /etc/pulse/default.pa

# null sink
.ifexists module-null-sink.so
load-module module-null-sink sink_name=Source
.endif

# virtual source
.ifexists module-virtual-source.so
load-module module-virtual-source source_name=VirtualMic master=Source.monitor
.endif
```
### Reload Systemd Daemon
After making these changes, reload the systemd user daemon:
```shell script
systemctl --user daemon-reload
```
### Enable and Start PulseAudio Service
```shell script
systemctl --user enable pulseaudio
systemctl --user start pulseaudio
```


## Install Radio Link
git clone https://github.com/safe-acid/TeamTalk5-RadioLink.git
```shell script
cd TeamTalk5-RadioLink
python3 -m venv .env
source .env/bin/activate
pip install -r requirements.txt
python3 setup.py
python3 radio.py --devices
```
### Setup you server settings and use Audio ID from Device Name: Virtual Source VirtualMic on Monitor of Null Output
```shell script
nano config.py
```
### run the bot
```shell script
python3 radio.py
```

