import vlc
from config import Config as conf

#VLC player class 
class VLCPlayer:
    def __init__(self):
        
        self.vlc_instance = vlc.Instance('--input-repeat=-1', '--network-caching=2000', '--file-caching=2000')
        self.vlc_player = None
        self.media = None
        self.volume = conf.max_volume
        #self.is_paused = False  # Flag to track pause state
        
        
    def play_url(self, url):
        # Handle existing playback (if any)
        
        if self.vlc_player:
            self.vlc_player.stop()
            self.vlc_player.release()
            self.media.release()  # Release the previous media object
           

        # Create new media and player
        self.media = self.vlc_instance.media_new(url)
        self.vlc_player = self.vlc_instance.media_player_new()
        self.vlc_player.set_media(self.media)
        self.set_volume(self.volume)
        self.vlc_player.play()
        #self.is_paused = True

    def stop(self):

        if self.vlc_player:  
            self.vlc_player.stop()
            self.vlc_player.release()
            self.vlc_player = None
            
            # Release the media object as well
            self.media.release()
            self.media = None 
            self.is_paused = False  # Reset pause state when stopping


    def set_volume(self, volume):
        # Ensure volume is within the range of 0 to MAX
        volume = max(0, min(int(volume), conf.max_volume))
        self.volume = volume
        # Set the volume for the media player
        if self.vlc_player:
            self.vlc_player.audio_set_volume(volume)
            
    # def pause_resume(self):
    #     if self.vlc_player:
    #         if self.is_paused:
    #             self.vlc_player.play()  # Resume playback
    #             self.is_paused = False
    #             print("Resumed playback")
    #         else:
    #             self.vlc_player.pause()  # Pause playback
    #             self.is_paused = True
    #             print("Paused playback")