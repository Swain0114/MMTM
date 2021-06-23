from gpiozero import LED, Button
from time import sleep
import picamera
import sys
import configparser


sys.path.append("../module")
import file

config = configparser.ConfigParser()
config.read_file(open("../configs/config.ini"))
default_video_recording_time = int(config["LOCAL_SETTING"]["VideoRecordingTime"])


led = LED(17)
button = Button(26)
camera = picamera.PiCamera()


def click_button_to_record():
    while True:
        button.wait_for_press()
        camera.resolution = (640, 480)
        led.on()

        h264_file_path = file.generate_video_file_path_with_datetime("h264")
        mp4_file_path = file.generate_video_file_path_with_datetime("mp4")

        camera.start_preview()
        camera.start_recording(h264_file_path)
        button.wait_for_press()
        camera.stop_recording()
        camera.stop_preview()
        file.convert_h264_to_mp4(h264_file_path, mp4_file_path)
        led.off()

        sleep(0.5)
        print("Done Successfully")
        button.wait_for_press()


def input_time_interval_to_record(time_interval_in_sec):
    while True:
        button.wait_for_press()
        camera.resolution = (640, 480)
        led.on()

        h264_file_path = file.generate_video_file_path_with_datetime("h264")
        mp4_file_path = file.generate_video_file_path_with_datetime("mp4")

        camera.start_preview()
        camera.start_recording(h264_file_path)
        if time_interval_in_sec:
            print("custom recording time: {}".format(time_interval_in_sec))
            sleep(time_interval_in_sec)
        else:
            print("default recording time: {}".format(default_video_recording_time))
            sleep(default_video_recording_time)
        camera.stop_recording()
        camera.stop_preview()
        file.convert_h264_to_mp4(h264_file_path, mp4_file_path)
        led.off()

        sleep(0.5)
        print("Done Successfully")
        button.wait_for_press()


def main(time_interval_in_sec=None):
    if time_interval_in_sec:
        input_time_interval_to_record(time_interval_in_sec)
    else:
        click_button_to_record()


if __name__ == "__main__":
    try:
        time_interval_in_sec = int(sys.argv[1])
        main(time_interval_in_sec)
    except:
        main()
