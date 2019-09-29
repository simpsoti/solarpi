# solarpi
This project displays current solar production using a Raspberry Pi, the SolarEdge inverter web-api and a UnicornHat HD from Pimoroni.

You will need to provide your own keys/ids for the Pushover and SolarEdge web-APIs in the config.json fle. You will also need to provide the name of a city near you.  This is used to determine time zone and sunrise/sunset times.

You will need to make sure the following python 3 modules are installed to be able to run the script:

solaredge
datetime
pytz
astral import
schedule
time
logging
unicornhathd
signal
colorsys
PIL
pushover
json

This program will display scrolling output of a sun graphic, the current power being generated and the energy generated so far that day.  A log file will be written in same directory as the python files. Every hour that the sun is up a notification will be sent via Pushover.
