# MMTM
Build camera and thermal camera with raspberry 4

# Hardware Settings
## Materials
- [Raspberry Pi 4 x1](https://www.raspberrypi.org/products/raspberry-pi-4-model-b/) 
- Button x2
- LED x1
- [RPi Camera (H) x1](https://www.waveshare.net/wiki/RPi_Camera_(H))
- [Thermal Camera x1](https://www.sparkfun.com/products/14843?_ga=2.80042583.1170791723.1624455150-1123456816.1624455150)
- [Resistor(220) x1](https://blog.jmaker.com.tw/arduino-tutorials-3/)
- Buzzer x1
## Assemble the Hardware
![Imgur](https://i.imgur.com/yoG1ex6.png)
- Click to Record Button
    - OUT: GPIO 26 (No.37)
    - VCC: 3v3 power (No.17)
    - GND: Ground (No.39)
- Blue LED
    - 5V power (No.4)
    - Ground (No.6)
    - GPIO 17 (No.11)
- Pi Camera
    - ![Camera Module Port](https://i.imgur.com/Ey6cOm5.png)
- Pithermal Camera
    - GND: Ground (No.25)
    - 3.3V: 3V3 power (No.1)
    - SDA: GPIO 3 (No.5)
    - SCL: GPIO 2 (No.3)
- Buzzer
    - Ground (No.9)
    - GPIO 22 (No.27)


# Software Settings
1. Add pictures folder to MMTM
2. Add videos folder to MMTM
3. Install MP4Box in order to convert h264 file to mp4
    - ```sudo apt-get install gpac```
4. [Setting Thermal Camera](https://makersportal.com/blog/2020/6/8/high-resolution-thermal-camera-with-raspberry-pi-and-mlx90640)
    - ```sudo apt-get install -y python-smbus```
    - ```sudo apt-get install -y i2c-tools```
    - ```sudo nano /boot/config.txt```
        - find ```dtparam=i2c_arm=on``` and modify it to ```dtparam=i2c_arm=on,i2c_arm_baudrate=400000```
    - ```sudo reboot```
5. Modify python package pithermalcam/pi_therm_cam.py save_image function, in order to save more image in the time interval, and remove watermark from image
    - add ```+ dt.datetime.now().strftime("%f")[:-5]``` below ```+ dt.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")```
    - comment out pithermalcam/pi_therm_cam.py (203 - 216 line)
        - find ```# For a brief period after saving, display saved notification```
    - find ```_process_raw_image``` and add ```.astype(np.unit8)``` to two ndimage.zoom functions
    - modify ```cv2.applyColorMap(self._raw_image, cmapy.cmap(self._colormap_list[self._colormap_index]))``` to ```cv2.applyColorMap(self._image, cmapy.cmap(self._colormap_list[self._colormap_index]))``` and add ```self._image = self._raw_image.astype(np.uint8)``` above of it.
    - find ```save_image``` function and add ```return fname```
6. Add ```export DISPLAY=:0.0``` to ~/.bashrc [Ref. link](https://github.com/opencv/opencv/issues/18461)


# Run Script
## Use Pi Camera to Record
- python3 apps/pi_camera_recording.py
    - click button to start recording
    - click button to stop recording
- python3 apps/pi_camera_recording.py {seconds}
    - click button to start recording
    - wait {seconds} and it would stop recording automatically

## Use Pi Thermal to Record
- python3 apps/pi_thermal_camera_recording.py
    - click button to start recording
    - click button to stop recording
- python3 apps/pi_thermal_camera_recording.py {seconds}
    - click button to start recording
    - wait {seconds} and it would stop recording automatically

## Use Pi Camera and Thermal to Record
- python3 apps/pi_recording.py
    - click button to start recording
    - click button to stop recording

