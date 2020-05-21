# Theremin 2.0

A digital theremin running on a Raspberry Pi.

## Setup

Run `python3 -m pip install -r requirements.txt`

## Usage

1. On the Pi, first run `python3 sensor.py reset` to set up the sensors properly.
2. Make `fbcp` and run `./fbcp &` to run the framebuffer copy program in the background.
3. On the host system, run `python3 synth.py`. Also make note of the host system's IP address.
4. On the Pi, run `python3 gui.py host_ip` where host_ip is replaced with the host system's IP.
5. Have fun!!
