import time
from gpiozero import LED
from gpiozero import Button

button = Button(18)

def is_pressed():
    return button.is_active