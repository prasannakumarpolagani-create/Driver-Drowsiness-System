import pygame

pygame.mixer.init()

def alarm():
    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.load("alarm.mp3")
        pygame.mixer.music.play()