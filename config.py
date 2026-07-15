class Config:
    #Version
    version = "2.3"
    sdk = "SDK 5.22a"
    
    #Server settings
    host = "tt5.live"
    tcpPort = 10333
    udpPort = 10333
    botName = "@RadioFM 🐳"
    username = "@radio"
    password = ""
    ChannelName = "/"
    ChannelPassword = ""
    radio_nick_icons = ["🐳", "⚡", "📻", "🎙️", "🎶", "🔊", "❤️", "⭐️", "🎲", "✨"]
    
    
    #Other settings
    #Audio Device ID - INT 
    audioInputID = 6
    #Default startup volume - INT
    default_volume = 30
    #Max default volume - INT     
    max_volume = 100 
    #PulseAudio sink for Linux FFmpeg output
    pulse_sink = "Source"
    #Network/audio buffer target for Linux streams, in seconds
    stream_buffer_seconds = 10
    #Only admin can operaate this bot - Boolean        
    admin = False    
    #Time in seconds to prevent message flood
    msgTimeDelay = 1
