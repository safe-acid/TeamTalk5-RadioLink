#
class Config:
    #Login settings
    host = "46.36.217.170"
    tcpPort = 10555
    udpPort = 10555
    botName = "_radioFM"
    username = "open"
    password = "open"
    ChannelName = "/_Audio bot"
    ChannelPassword = ""
    
    #Other settings
    audioInputID = 6        #Virtual audio input                        - INT 
    max_volume = 50         #Max default volume                         - INT 
    admin = True            #Admin could change/add stations            - Boolean
    operator = True         #Chanel operatoor could change/add stations - Boolean
    registered_user = True  #Requstered user could change/add stations  - Boolean
    
    
    
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