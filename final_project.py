# IMPORT ALL MY STUFF
import RPi.GPIO as GPIO
import random
from time import sleep, strftime
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.virtual import viewport
from luma.led_matrix.device import max7219
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, CP437_FONT

# DOT MATRIX SETUP
serial = spi(port=0, device=0, gpio=noop())
device = max7219(serial, width=32, height=8, block_orientation=-90)
device.contrast(4)
virtual = viewport(device, width=32, height=16)

#Button Setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(21, GPIO.IN)

# For DOT MATRIX
# VCC = 5v pin
# GND = GND pin
# DIN = MOSI pin (not to be confused with "MISO")
# CS = CEO pin
# CLK = SCLK pin

# For Digital Button
# S = GPIO pin 21
# V = 5v pin
# G = GND pin

winning_nums = ["0000", "1111", "2222", "3333", "4444", "5555", "6666", "7777", "8888", "9999"]

def get_nums():
    w = str(random.randint(0,9))
    x = str(random.randint(0,9))
    y = str(random.randint(0,9))
    z = str(random.randint(0,9))
    num = w+x+y+z
    return num

def final_dice():
    num = get_nums()
    with canvas(virtual) as draw:
            text(draw, (2, 0), num, fill="white", font=proportional(CP437_FONT))
    sleep(1)
    return num

def roll():
    i = 17
    r = 0.0
    hehe = random.randint(1,12)
    while i != 0:
        #i to slow down and hehe to display at least 1 time where all nums are same
        num = get_nums()
        if i != hehe:
            with canvas(virtual) as draw:
                text(draw, (2, 0), num, fill="white", font=proportional(CP437_FONT))
                sleep(0.1 + r)
        else:
            with canvas(virtual) as draw:
                text(draw, (2, 0), winning_nums[random.randrange(1, len(winning_nums))], fill="white", font=proportional(CP437_FONT))
                sleep(0.1 + r)
        i -= 1
        r += 0.01 + (1/5 * r)
    sleep(0.8 + r)

# If is a winning number
def winner(win):
    w = 5
    while w != 0:
        sleep(0.4)
        show_message(device, "JACKPOT YOU'RE A WINNER!", fill="white", font=proportional(CP437_FONT), scroll_delay=0.04)
        sleep(0.5)
        with canvas(virtual) as draw:
            text(draw, (2, 0), win, fill="white", font=proportional(CP437_FONT))
        sleep(0.4)
        show_message(device, "     ", fill="white", font=proportional(CP437_FONT), scroll_delay=0.001)
        w -= 1
    main()

#If not a winning number
def loser(loss):

    # alternate between loosing number and message 
    l = 5
    while l != 0:
        sleep(0.4)
        show_message(device, "Better luck next time!", fill="white", font=proportional(CP437_FONT), scroll_delay=0.04)
        sleep(0.5)
        with canvas(virtual) as draw:
            text(draw, (2, 0), loss, fill="white", font=proportional(CP437_FONT))
        sleep(0.8)
        show_message(device, "     ", fill="white", font=proportional(CP437_FONT), scroll_delay=0.001)
        l -= 1
    #call back to restart the loop
    main()

#When button is pressed
def button_pressed():
    roll()
    sleep(0.1)
    num = final_dice()

    #Flash number you got
    e = 3
    while e != 0:
        show_message(device, "     ", fill="white", font=proportional(CP437_FONT), scroll_delay=0.02)
        with canvas(virtual) as draw:
            text(draw, (2, 0), num, fill="white", font=proportional(CP437_FONT))
        sleep(0.4)
        e -= 1

    #Check if you won or not
    if num in winning_nums:
        winner(num)
    else:
        loser(num)

#used to keep in loop to continue gambling
def main():
    #keep in loops till buton is pressed
    while True:
        if GPIO.input(21) == 1:
            continue
        elif GPIO.input(21) == 0:
            break
    button_pressed()

# Start code after defining everything
try:
    main()

except KeyboardInterrupt:
    GPIO.cleanup()