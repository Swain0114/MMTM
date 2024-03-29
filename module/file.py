import pytz
from datetime import datetime
from subprocess import call
import configparser
import glob
import cv2

config = configparser.ConfigParser()
config.read_file(open("./configs/config.ini"))
str_of_timezone = config["LOCAL_SETTING"]["Timezone"]
video_file_path = config["LOCAL_SETTING"]["VideoFilePath"]
picture_file_path = config["LOCAL_SETTING"]["PictureFilePath"]
avi_temp_video_file_path = config["LOCAL_SETTING"]["AviTempVideoFilePath"]

print("time zone setting is {}".format(str_of_timezone))


def generate_video_file_path_with_datetime(file_type, camera_type, is_time_interval):
    file_name = datetime.now(pytz.timezone(str_of_timezone)).strftime("%Y%m%d_%H%M%S")
    if camera_type == "pi_cam":
        if is_time_interval:
            file_path = "{}video_Ns_{}.{}".format(video_file_path, file_name, file_type)
        else:
            file_path = "{}video_button_{}.{}".format(
                video_file_path, file_name, file_type
            )
    elif camera_type == "pi_thermal":
        if is_time_interval:
            file_path = "{}video_thermal_Ns_{}.{}".format(
                video_file_path, file_name, file_type
            )
        else:
            file_path = "{}video_thermal_button_{}.{}".format(
                video_file_path, file_name, file_type
            )

    return file_path


def convert_h264_to_mp4(h264_file_name, mp4_file_name):
    convert_command = "MP4Box -add {} {}".format(h264_file_name, mp4_file_name)

    call([convert_command], shell=True)
    print("Video converted!")

    delete_h264_command = "rm {}".format(h264_file_name)
    call([delete_h264_command], shell=True)
    print("h264 file deleted!")

    return True


def convert_jpg_to_avi():
    img_array = []
    for file_name in glob.glob("{}/*.jpg".format(picture_file_path)):
        img = cv2.imread(file_name)
        height, width, layers = img.shape
        size = (width, height)
        img_array.append(img)

    out = cv2.VideoWriter(
        "{}temp.avi".format(video_file_path),
        cv2.VideoWriter_fourcc(*"DIVX"),
        4,
        size,
    )

    for i in range(len(img_array)):
        out.write(img_array[i])
    out.release()

    return True


def convert_avi_to_mp4(mp4_file_name):
    convert_command = "MP4Box -add {} {}".format(
        avi_temp_video_file_path, mp4_file_name
    )
    # mp4box -add file.avi new_file.mp4

    call([convert_command], shell=True)
    print("Video converted!")

    for file_name in glob.glob("{}/*.jpg".format(picture_file_path)):
        delete_jpg_command = "rm {}".format(file_name)
        call([delete_jpg_command], shell=True)
        # print("jpg file deleted!")

    print("all jpg files deleted")

    delete_avi_command = "rm ./videos/temp.avi"
    call([delete_avi_command], shell=True)

    print("temp.avi files deleted")
