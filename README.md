# Embedded-CW1

This repository includes the code for the first coursework of the module Embedded Systems at Imperial College London. The goal was to design a useful IoT device with commercial prospects.

Credits to alexwillie as collaborator
## Specifications

Our concept was to make a device that constantly measures the position of your back and neck and and classifies if the user is in a bad or good position. The sensor data is then stored remotely on a server and the user can then acces this on a website to see a graph of his performance over time.

## Structure
```
├── Documents
      ├── simpletest.py
      └── simpletest.py.save
├── Rpi_backup                      # Files on Rpi zero
├── AmazonRootCA1.pem               # Certificate for server
├── MQTT_new.py                     # MQTT messaging Systems
├── plot_sensor.py                  # Python file on the server to graph data
└── sensor.py                       # getting sensor data                   
```                
