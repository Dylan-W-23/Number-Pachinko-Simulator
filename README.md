# Number Pachinko Simulator

## Overview
Number Pachinko Simulator aims to simulate a number pachinko machine based on the number of attempts and the chance (fraction or percentage) of hitting a jackpot.

## Definition of Pachinko
Pachinko is a mechanical game made in Japan for arcades and gambling, offering modern mechanical and electrical components compared to western slot machines that offer low-stakes and low-strategy gambling.

See [Wikipedia](https://en.wikipedia.org/wiki/Pachinko) for more information.

## Program Info and License
This program is based on Python using Tkinter, random, and time modules, and is licensed under GNU General Public License v3.0.

## How to Use
Open the Python file using a command line or an Integrated Development Environment (IDE). For command line prompts, ensure the directory contains the NumPachinkoSimulator file and enter `python3 NumPachinkoSimulator.py`.

## How it Works
1. The user chooses a mode to input the chance value, using either fraction-based or percentage-based.
2. The user then inputs the value of the chance, typically less than a whole number (one), using the determined mode. For example, 1/20.0 as a fraction, or 5% as a percentage.
3. The simulation begins by showing another window with 3 big numbers and an attempts counter. Eventually, the simulation begins with the numbers randomising until it generates a combination based on the hit value against the chance. If the 3 numbers do not match, it indicates a miss and repeats the randomisation on the next attempt.
4. The simulation will continue to randomise until all 3 numbers match, in which it hits the jackpot chance, and the simulation will end, presenting the number of attempts it took to complete the specified chance. The user will be able to input again if they choose to continue.

## How Chances are Determined
Chances are determined with a random decimal number against a hit value. The chance is successful (is a hit) when the random value is either equal or lower than the hit value.

The number is randomized as a decimal between zero and the maximum number determined by the user input.

## Chance Mode
Chance can be determined using either fraction or percentage.
- <b>Fraction</b>: Numerator and denominator values can be determined using the format: `<Numer>/<Denom>`. The numerator becomes the hit value and the denominator will be the max value for the random range (i.e. between zero and the denominator).
- <b>Percent</b>: A value between 0-100 can be set for the percentage. The value is then divided by 100 to convert into decimal form and provide the hit value. The max range value automatically becomes one.