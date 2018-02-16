# GM01
A simple Python Server for the GSM Camera Called GM01

This server is opening a Port (8710) for the GSM Camera to connect to.

The Protocol used: 
http://tr.iconcox.com/uploads/soft/140916/1-140916014342.pdf

The received Photos are saved under fotos and are uploaded to google drive by gdrive:
https://github.com/prasmussen/gdrive

To use this serve be shure your computer/server chan be reached from its local IP address over port 8710.

Send an SMS with the following text to your Camera: 
SERVER,0,YOUR_IP_ADDRESS,8710,0#
