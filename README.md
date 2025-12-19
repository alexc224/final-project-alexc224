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
   - DIN to
   -  to MOSI
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
