import sys, os, platform, ctypes, logging, time, threading, argparse, importlib, re, requests
import stations, radio_user
from config import Config as conf
from typing import Optional
from messages import messages
from vlc_player import VLCPlayer as vlc


script_dir = os.path.dirname(os.path.abspath(__file__))
system = platform.system()
   # Construct the full path to the dynamic library file MAC/Linux/Win
if system == "Darwin":
    library_dir = os.path.join(script_dir, "sdk/Library/TeamTalk_DLL")
    library_path = os.path.join(library_dir, "libTeamTalk5.dylib") 
    print("run on Darwin")
elif system == "Linux":
    library_dir = os.path.join(script_dir, "sdk/Library/TeamTalk_DLL")
    library_path = os.path.join(library_dir, "libTeamTalk5.so")
    print("run on Linux")
elif system == "Windows":
    library_dir = os.path.join(script_dir, "sdk/Library/TeamTalk_DLL")
    library_path = os.path.join(library_dir, "TeamTalk5.dll")
    print("run on Windows")
    
# Load the dynamic library using ctypes
try:
    ctypes.cdll.LoadLibrary(library_path)
except OSError as e:
    print(f"Error loading the library: {e}")
    sys.exit(1)
    
# Add logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

 
from sdk.Library.TeamTalkPy import TeamTalk5
from TeamTalk5 import *

class TTClient:
    def __init__(self, host, tcpPort, udpPort, nickName, userName, password):
        self.host = host
        self.tcpPort = tcpPort
        self.udpPort = udpPort
        self.nickName = nickName
        self.userName = userName
        self.password = password
        self.tt = TeamTalk5.TeamTalk()
        self.tt.onConnectSuccess = self.onConnectSuccess
        self.tt.onConnectionLost = self.onConnectionLost
        self.tt.onCmdMyselfLoggedIn = self.onCmdMyselfLoggedIn
        self.tt.onCmdUserTextMessage = self.onCmdUserTextMessage
        self.connected = False   # Flag to track connection status
        self.reconnect_delay =  10 # Set reconnect interval to 10 seconds
        self.reconnect_thread = threading.Thread(target=self.reconnect_loop, daemon=True)
        self.reconnect_thread.start()
        self.vlc = vlc()
        
    
        
    def play_radio(self, radio_choice):
       
        radio_urls = stations.Radio.radio_urls
        if radio_choice in radio_urls:
            url = radio_urls[radio_choice]
            try:
                self.vlc.stop()  # Stop any existing playback
                self.vlc.play_url(url)
                self.enable_voice_transmission()
               
            except Exception as e:  # Catch potential errors
                logging.error(f"Error playing radio: {e}")
            

            # Change nickname status with radio
            radio_names = stations.Radio.radio_names
            if radio_choice in radio_names:
                radio_name = radio_names[radio_choice]
                self.tt.doChangeStatus(0, ttstr(f"{self.get_message('station')} - {radio_name}. {self.get_message('info')}"))
   
            
    def radio_stop(self):
        self.disable_voice_transmission()
        return self.vlc.stop()
     
 
    def play_radio_on_request(self, msg):
        self.radio_stop()
        time.sleep(1)
        self.enable_voice_transmission()
        self.play_radio(msg)
    
    def enable_voice_transmission(self) -> None:
        self.tt.enableVoiceTransmission(True)
        
    def disable_voice_transmission(self) -> None:
        self.tt.enableVoiceTransmission(False)
    
    def start(self):
        self.connect()
                   
    def connect(self):
        self.tt.connect(self.host, self.tcpPort, self.udpPort)

    def onConnectSuccess(self):
        self.connected = True #Connection established
        self.tt.doLogin(self.nickName, self.userName, self.password, ttstr("ttsamplepy"))
        time.sleep(1)
              
    def onConnectionLost(self):
        self.radio_stop()
        self.connect()
        self.connected = False
        logger.info("Connection lost.")
        
    def set_input_device(self, id: int) -> None:
        self.tt.initSoundInputDevice(id)   
           
    def quit(self,fromUserID=None,fromUserName=None, msg=None):
        time.sleep(1)
        self.radio_stop()   
        time.sleep(1)
        self.dynamic_nick()
        self.vlc.stop()
        if fromUserID != None and fromUserName != None and msg != None:
            self.send_message(f"{ttstr(fromUserName)} {self.get_message('requested')} {msg}", fromUserID, 2) 
            self.send_message(self.get_message("bot_sleeping"),fromUserID,1)  
            
    
    def get_message(self, key):
        if key in messages:
            return messages[key][current_language]
        else:
            # Handle missing message key
            return "Message not found."
    
    def dynamic_nick(self):
            self.change_nickname(f"{conf.botName}" )
            self.tt.doChangeStatus(0, ttstr(self.get_message("info")))
            
    def onCmdMyselfLoggedIn(self,userID, userAccount):
        print(f"Hello {userAccount.szUsername}. Your User ID is {userID}")
        time.sleep(2.0)
        channelID = self.tt.getChannelIDFromPath(ttstr(conf.ChannelName))
        print(channelID)
        time.sleep(1.0)
        self.tt.doJoinChannelByID(channelID, ttstr(conf.ChannelPassword))
        self.tt.doChangeStatus(0, ttstr(self.get_message("info")))     
        self.set_input_device(conf.audioInputID)
      
    def reconnect_loop(self):
        while True:   
                if not self.connected:
                    logger.info("Attempting to reconnect...")
                    self.tt.disconnect()
                    time.sleep(2)
                # Attempt to reconnect
                    self.connect()
                time.sleep(self.reconnect_delay)  
    
    def onChannelMessage(self, fromUserID, fromUserName, channelID, msgText):
         print(f"Channel message in channelid {ttstr(channelID)} from userid {ttstr(fromUserID)} username: {ttstr(fromUserName)} {ttstr(msgText)}")

    def change_nickname(self, nickname):
           self.tt.doChangeNickname(ttstr(nickname))
    
    def onCmdUserTextMessage(self, message):
        msgType = message.nMsgType
        if msgType == TeamTalk5.TextMsgType.MSGTYPE_USER:
            self.onUserMessage(message.nFromUserID, message.szFromUsername, message.szMessage)
        if msgType == TeamTalk5.TextMsgType.MSGTYPE_CHANNEL:
            self.onChannelMessage(message.nFromUserID, message.szFromUsername, message.nChannelID, message.szMessage)
        if msgType == TeamTalk5.TextMsgType.MSGTYPE_BROADCAST:
            self.onBroadcastMessage(message.nFromUserID, message.szFromUsername, message.szMessage)  
    
    #grabbing users in channels
    def get_users_in_channels(self):
          user_ids = []
          bot_chanelId = self.tt.getMyChannelID()
          users_in_channel = self.tt.getChannelUsers(bot_chanelId)
          #Check if users_in_channel is not None and access user information accordingly
          if users_in_channel is not None:
           for user in users_in_channel:
            # Append each user ID to the list
                user_ids.append(user.nUserID)       
          return user_ids
      
    #checking is user who sent message in channel
    def userID_inChannel(self, id_to_check):
    # Call the function to get the list of user IDs
       user_ids = self.get_users_in_channels()    
       if id_to_check in user_ids:
          return True
       return False 
   
    def isUserAdmin(self, user_id):
        user = self.tt.getUser(user_id)
        if user.uUserType == 2:
            return True
        return False
    
    def anonymous(self, szFromUsername):
        if len(szFromUsername) == 0:
            return False
        return True      
    
    def send_message(
        self, text: str, user: Optional[User] = None, type: int = 1
        ) -> None:
        message = TeamTalk5.TextMessage()
        message.nFromUserID = self.tt.getMyUserID()
        message.nMsgType = type
        message.szMessage = ttstr(text)
       
        if type == 1:
            if isinstance(user, int):
                message.nToUserID = user
            else:
                message.nToUserID = user.id
        elif type == 2:
                message.nChannelID = self.tt.getMyChannelID()
        self.tt.doTextMessage(message)
    
    #Radio channel message
    def send_radio_menu(self, fromUserID):
        # from radio import Radio
        importlib.reload(stations)
        message_lines = [self.get_message("help_top")]  # help message header
        for number, name in stations.Radio.radio_names.items():
            message_lines.append(f"{number}: {name}")  # Build each line
        message = "\n".join(message_lines) 
        self.send_message(message, fromUserID, 1)  
        
    def onUserMessage(self, fromUserID, fromUserName, msg):
        anonymous = self.anonymous(fromUserName)
        userInChanel = self.userID_inChannel(fromUserID)
        msg = ttstr(msg)
        time.sleep(1.5)
        if anonymous and userInChanel:
            if  msg.lower() == "v":
                self.send_message(self.get_message("about"),fromUserID,1) 
             # RADIO Selections
            if msg.lower() == "h":
                self.send_radio_menu(fromUserID)
                self.send_message(self.get_message("help"),fromUserID,1) 
            else:
                    try:
                        station_number = int(msg.lower())  
                        if station_number == 21:
                           
                            importlib.reload(radio_user)
                             # Access the latest value
                            custom_radio_url = radio_user.custom_radio_url
                            custom_radio_name = radio_user.custom_radio_name
                            
                            try:
                                self.vlc.stop()  # Stop any existing playback
                                self.vlc.play_url(custom_radio_url)
                                self.enable_voice_transmission()
                                self.tt.doChangeStatus(0, ttstr(f"Станция - {custom_radio_name}. \"h\" справка. "))
                            
                            except Exception as e:  # Catch potential errors
                                logging.error(f"Error playing radio: {e}")
                           
                        elif 1 <= station_number <= len(stations.Radio.radio_urls):  # Check if valid number
                            self.enable_voice_transmission()
                            self.play_radio(str(station_number))  # Convert back to string
                       
                               
                    except ValueError:
                    # Handle cases where the message isn't a number
                        pass       
                              
            if msg.lower()[:3] == "add":
            
                # Extracting name and URL from the message using regex
                match = re.match(r'add\s+(\w+)\s+(https?://\S+\.m3u8)', msg, re.IGNORECASE)

                if match:
                    name = match.group(1)  # Extracting the name
                    url = match.group(2)   # Extracting the URL
                    response = requests.head(url)
                    
                    if response.status_code in [200, 301]:
                        print("URL is valid and returns 200 or 301 status code.")
                        
                        # Open the 'radio_user.py' file for appending
                        with open('radio_user.py', 'w') as file:
                            file.write(f'custom_radio_url = "{url}"\n')   
                            name = name[:10]
                            file.write(f'custom_radio_name = "{name}"\n')
                            self.send_message(f"Радиостанция:{name} добавлена", fromUserID, 1)
                            print("New radio URL and name added to the radio.py file.")
                else:
                            self.send_message(f"URL does not return 200 or 301 status code.", fromUserID, 1)
                            print("URL does not return 200 or 301 status code.")

            # Check for volume command first
            elif msg.lower().startswith("v") and len(msg) > 1:  # Check for at least one digit after "v"
                try:
                    volume_level = int(msg[1:])  # Extract digits after "v"
                    if 0 <= volume_level <= conf.max_volume:
                        self.vlc.set_volume(volume_level)
                        self.send_message(f"{self.get_message('vol_set_to')}  {volume_level}", fromUserID, 2)
                    else:
                        self.send_message(self.get_message("wrong_volume"), fromUserID, 1)
                except ValueError:
                    self.send_message((self.get_message("wrong_volume_format")), fromUserID, 1)
                 
                
           
            elif msg.lower() == "q":
                self.radio_stop()
                self.quit(fromUserID,fromUserName, msg)
                
          
        
    
    def defaultAudioDevices(self):
        msg = "\n\nDefault Audio Input Devices:\n"
        for device in self.tt.getSoundDevices():
            msg += f"Device ID: {device.nDeviceID},\n" \
               f"Sound System: {device.nSoundSystem},\n" \
               f"Device Name: {device.szDeviceName.decode('utf-8')},\n\n " \

        print(msg)
        
if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser(description='Process some integers.')
        parser.add_argument('--language', action='store', help='Select language (ru or en)', default="")
        parser.add_argument('--devices', action='store_true', help='Display default audio devices')
        args = parser.parse_args()
        
        # Set current_language based on the argument
        if args.language == "ru":
            current_language = "ru"
        #if need your other language     
        elif args.language == "en":
            current_language = "en"
        else:
            # Handle unsupported languages (optional: log a warning or provide default language)
            current_language = "en"  # Assuming default to English
        
        ttClient = TTClient(ttstr(conf.host), conf.tcpPort, conf.udpPort, ttstr(conf.botName), ttstr(conf.username), ttstr(conf.password))
        
        if args.devices:
            ttClient.defaultAudioDevices()
        else:
            # Start the TeamTalk client if not displaying devices
            time.sleep(1.5)
            ttClient.start()
            while True:
                ttClient.tt.runEventLoop()
                
    except KeyboardInterrupt:
        running = False
        