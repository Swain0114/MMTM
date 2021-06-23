# MMTM
Build camera and thermal camera with raspberry 4

# Hardware Settings
## Materials
- [Raspberry Pi 4 x1](https://www.raspberrypi.org/products/raspberry-pi-4-model-b/) 
- Button x2
- LED x1
- [RPi Camera (H)](https://www.waveshare.net/wiki/RPi_Camera_(H))
- [Thermal Camera](https://www.sparkfun.com/products/14843?_ga=2.80042583.1170791723.1624455150-1123456816.1624455150)
- [Resistor(220) x1](https://blog.jmaker.com.tw/arduino-tutorials-3/)

# Software Settings
1. Add pictures folder to MMTM
2. Add videos folder to MMTM
3. Modify python package pithermalcam/pi_therm_cam.py save_image function
    - add ```+ dt.datetime.now().strftime("%f")[:-5]``` below ```+ dt.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")```
    - comment out pithermalcam/pi_therm_cam.py (203 - 216 line)

# Run Script
## Use Pi Camera to Record
python3 apps/pi_camera_recording.py
## Use Pi Camera to Record
python3 apps/pi_thermal_camera_recording.py