from gpiozero import LED, Button
from time import sleep
import picamera
import sys
import cv2
from pithermalcam.pi_therm_cam import pithermalcam
from subprocess import call
import sys
import configparser

config = configparser.ConfigParser()
config.read_file(open("./configs/config.ini"))
picture_file_path = config["LOCAL_SETTING"]["PictureFilePath"]
sys.path.append("./module")
import file


led = LED(17)
button = Button(26)
camera = picamera.PiCamera()
thermal_cam = pithermalcam(output_folder=picture_file_path)


def click_button_to_record():
    while True:
        button.wait_for_press()
        camera.resolution = (640, 480)
        led.on()
        print("start recording...")

        pi_camera_h264_file_path = file.generate_video_file_path_with_datetime(
            "h264", "pi_cam", False
        )
        pi_camera_mp4_file_path = file.generate_video_file_path_with_datetime(
            "mp4", "pi_cam", False
        )
        pi_thermal_mp4_file_path = file.generate_video_file_path_with_datetime(
            "mp4", "pi_thermal", False
        )

        camera.start_preview()
        print("pi camera start recording...")
        camera.start_recording(pi_camera_h264_file_path)
        while True:
            print("pi thermal camera start recording...")
            thermal_cam.display_next_frame_onscreen()
            thermal_cam.save_image()
            if button.is_pressed:
                break

        button.wait_for_press()
        camera.stop_recording()
        camera.stop_preview()

        file.convert_h264_to_mp4(pi_camera_h264_file_path, pi_camera_mp4_file_path)
        print("pi camera end recording...")

        cv2.destroyAllWindows()
        file.convert_jpg_to_avi()
        file.convert_avi_to_mp4(pi_thermal_mp4_file_path)
        print("pi thermal camera end recording...")
        led.off()

        sleep(0.5)
        print("Done Successfully")
        button.wait_for_press()

if __name__ == "__main__":
    click_button_to_record()
