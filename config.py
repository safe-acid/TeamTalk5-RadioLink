class Config:
    version = "1.0"
    
    #Login settings
    host = "46.36.217.170"
    tcpPort = 10555
    udpPort = 10555
    botName = "_botRadioFM"
    username = "open"
    password = "open"
    ChannelName = "/_Audio bot"
    ChannelPassword = ""
    
    #Other settings
    #Audio Device ID - INT 
    audioInputID = 3  
    #Max default volume - INT     
    max_volume = 50 
    #Admin could change/add stations, default -> registered user - Boolean        
    admin = False           


    #Example
    # host = "46.36.217.170"
    # tcpPort = 10555
    # udpPort = 10555
    # botName = "_radioFM"
    # username = "open"
    # password = "open"
    # ChannelName = "/_Audio bot"
    # #ChannelPassword = "1112"
    # ChannelPassword = "private"
    # audioInputID = 6
    # max_volume = 50