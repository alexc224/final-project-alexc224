# final-project-alexc224

## What it is
A slot machine that displays numbers on a LED Dot Matrix in a slot machine style.

## What is needed

- Raspberry Pi
- 8x32 LED Dot Matrix (one solid color)
- Jumper Wires
- Digital Button

## How to start
1) With jumper wires, Led Dot Matrix and your Pi connect wires to the following:
   - VCC to 5V
   - GND to Ground
   - DIN to
   -  to MOSI
   - CLK to
2) With jumper wires, digital button and pi; connect wires to the following:
   - V to 5v
   - G to Ground
   - S to GPIO 21

## Getting Pi ready
1) If you haven't already, install the ```venv``` program into the folder where the code will be with ```sudo apt install venv```
2) After installing ```venv```, create a virtual enviorment in the folder with ```python3 -m venv venv```. This should create a folder inside of your folder/directory.
3) To activate the virtual enviorment run the command ```source venv/bin/activate```. Remember to be in the same directory that you activated the virutal enviorment in.
