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
video_file_path = config["LOCAL_SETTING"]["VideoFilePath"]
sys.path.append("./module")
import file


led = LED(17)
button = Button(26)
camera = picamera.PiCamera()
thermal_cam = pithermalcam(output_folder=picture_file_path)


def click_button_to_record():
    print("start recording...")
    while True:
        button.wait_for_press()
        camera.resolution = (640, 480)
        led.on()

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
        camera.start_recording(pi_camera_h264_file_path)
        out = cv2.VideoWriter(
            "{}temp.avi".format(video_file_path),
            cv2.VideoWriter_fourcc(*"DIVX"),
            4,
            (800, 600),
        )
        while True:
            thermal_cam.display_next_frame_onscreen()
            thermal_file_name = thermal_cam.save_image()
            img = cv2.imread(thermal_file_name)
            out.write(img)
            delete_jpg_command = "rm ./pictures/*.jpg"
            call([delete_jpg_command], shell=True)

            if button.is_pressed:
                break

        button.wait_for_press()
        camera.stop_recording()
        camera.stop_preview()

        file.convert_h264_to_mp4(pi_camera_h264_file_path, pi_camera_mp4_file_path)
        print("pi camera end recording...")

        cv2.destroyAllWindows()
        file.convert_avi_to_mp4(pi_thermal_mp4_file_path)
        print("pi thermal camera end recording...")
        led.off()

        sleep(0.5)
        print("Done Successfully")
        button.wait_for_press()


if __name__ == "__main__":
    click_button_to_record()
