#!python3
from gtts import gTTS
import contextlib
import io

with contextlib.redirect_stdout(None):
    import pygame
  
def alert_sound(text):
    sound = io.BytesIO()
    
    gt = gTTS(text)
    gt.write_to_fp(sound)
    
    sound.seek(0)
    
    pygame.mixer.init()
    pygame.mixer.music.load(sound)
    pygame.mixer.music.play()
    
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

alert_sound('Error in page 3')
print('hello')