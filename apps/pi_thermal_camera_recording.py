from gpiozero import LED, Button
from time import sleep
from datetime import datetime
import cv2
from pithermalcam.pi_therm_cam import pithermalcam
import configparser
from subprocess import call
import sys

sys.path.append("./module")
import file

config = configparser.ConfigParser()
config.read_file(open("./configs/config.ini"))
picture_file_path = config["LOCAL_SETTING"]["PictureFilePath"]
default_video_recording_time = int(config["LOCAL_SETTING"]["VideoRecordingTime"])
video_file_path = config["LOCAL_SETTING"]["VideoFilePath"]

thermal_cam = pithermalcam(output_folder=picture_file_path)
led = LED(17)
button = Button(26)


def click_button_to_record():
    while True:
        button.wait_for_press()
        led.on()

        mp4_file_path = file.generate_video_file_path_with_datetime(
            "mp4", "pi_thermal", False
        )

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

        cv2.destroyAllWindows()
        file.convert_avi_to_mp4(mp4_file_path)

        led.off()

        sleep(0.5)
        print("Done Successfully")
        button.wait_for_press()


def input_time_interval_to_record(time_interval_in_sec):
    while True:
        button.wait_for_press()
        led.on()

        mp4_file_path = file.generate_video_file_path_with_datetime(
            "mp4", "pi_thermal", True
        )

        start_time = datetime.now()
        print("start time {}".format(start_time))
        time_diff_in_sec = 0  # init

        out = cv2.VideoWriter(
            "{}temp.avi".format(video_file_path),
            cv2.VideoWriter_fourcc(*"DIVX"),
            4,
            (800, 600),
        )

        while time_diff_in_sec < time_interval_in_sec:
            print("time diff in sec - {}".format(time_diff_in_sec))
            thermal_cam.display_next_frame_onscreen()
            thermal_file_name = thermal_cam.save_image()
            img = cv2.imread(thermal_file_name)
            out.write(img)
            delete_jpg_command = "rm ./pictures/*.jpg"
            call([delete_jpg_command], shell=True)

            time_diff_in_sec = (datetime.now() - start_time).total_seconds()

        cv2.destroyAllWindows()
        file.convert_avi_to_mp4(mp4_file_path)
        led.off()

        sleep(0.5)
        print("Done Successfully")
        button.wait_for_press()


def main(time_interval_in_sec=None):
    if time_interval_in_sec:
        print("start time interval recording")
        input_time_interval_to_record(time_interval_in_sec)
    else:
        print("start click button recording")
        click_button_to_record()


if __name__ == "__main__":
    try:
        time_interval_in_sec = int(sys.argv[1])
        main(time_interval_in_sec)
    except:
        main()
