from gpiozero import LED, Button
from time import sleep
import cv2
from pithermalcam.pi_therm_cam import pithermalcam
import configparser
from subprocess import call
import sys

sys.path.append("../module")
import file

config = configparser.ConfigParser()
config.read_file(open("../configs/config.ini"))
picture_file_path = config["LOCAL_SETTING"]["PictureFilePath"]

thermal_cam = pithermalcam(output_folder=picture_file_path)
led = LED(17)
button = Button(26)


def click_button_to_record():
    while True:
        button.wait_for_press()
        led.on()

        mp4_file_path = file.generate_video_file_path_with_datetime("mp4")

        while True:
            thermal_cam.display_next_frame_onscreen()
            thermal_cam.save_image()
            if button.is_pressed:
                break

        file.convert_jpg_to_avi()
        file.convert_avi_to_mp4(mp4_file_path)
        led.off()

        sleep(0.5)
        print("Done Successfully")
        button.wait_for_press()


if __name__ == "__main__":
    click_button_to_record()
