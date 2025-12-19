# final-project-alexc224

## What it is
A slot machine that displays numbers on a LED Dot Matrix in a slot machine style.

## What is needed

- Raspberry Pi
- 8x32 MAX7219 LED Dot Matrix (one solid color)
- Jumper Wires
- Digital Button

## Making connections
1) With jumper wires, Dot Matrix, and your Pi; connect wires to the following:
   - VCC to 5V
   - GND to Ground
   - DIN to MOSI
   - CS to CEO
   - CLK to SCLK
2) With jumper wires, digital button, and the Pi; connect wires to the following:
   - V to 5v
   - G to Ground
   - S to GPIO 21

## Getting Pi ready
1) If you haven't already, install the ```venv``` program into the folder where the code will be with ```sudo apt install venv```
2) After installing ```venv```, create a virtual enviorment in the folder with ```python3 -m venv venv```. This should create a folder inside of your folder/directory.
3) To activate the virtual enviorment run the command ```source venv/bin/activate```. Remember to be in the same directory that you activated the virutal enviorment in.
4) In the virtual enviorment install the later version of the ```luma.led_matrix``` package with ```sudo python3 -m pip install --upgrade luma.led_matrix```
5) Make sure you have the SPI configured with ```ls -l /dev/spi*``` and it should reply with ```/dev/spidev0.0  /dev/spidev0.1```. If it is not consult [https://learn.sparkfun.com/tutorials/raspberry-pi-spi-and-i2c-tutorial#spi-on-pi](url) to configure the SPI.

## The Code
1) In the same folder that you have the venv package, make a python script in the terminal by inputting ```touch slot.py``` or something similar. The only thing that is absolitely needed is that its a python file.
2) Copy and paste the following code into the file using an editor or the nano tool. All notes on the workings of the code should be in the comments:

```
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
```
