from math import sqrt
import cv2
from tflite_support.task import core
from tflite_support.task import processor
from tflite_support.task import vision
import utils

base_options = core.BaseOptions(
    file_name='../model/model.tflite', use_coral=False, num_threads=4)
detection_options = processor.DetectionOptions(
    max_results=10, score_threshold=0.15, category_name_allowlist=['cat'])
options = vision.ObjectDetectorOptions(
    base_options=base_options, detection_options=detection_options)
detector = vision.ObjectDetector.create_from_options(options)


def compare_bounding_box(bounding_boxA, bounding_boxB):
    """
    compare bounding box coordinate

    Args:
        bounding_boxA: bounding box A
        bounding_boxB: bounding box B
    """

    x_distance = abs(bounding_boxA.origin_x - bounding_boxB.origin_x)
    y_distance = abs(bounding_boxA.origin_y - bounding_boxB.origin_y)

    distance = sqrt(x_distance ** 2 + y_distance ** 2)

    if (distance > 50):
        return True
    return False


def detect_algo(current_detections, previous_detections):
    """
    Algo of detect mouse motion

    Args:
        current_detections: current frame of detection results
        previous_detections: previous frame of detection results
    """

    if (len(current_detections) != len(previous_detections)):
        return True
    elif ((current_detections) == len(previous_detections)):
        for current, previous in zip(current_detections, previous_detections):
            return compare_bounding_box(
                current.bounding_box,
                previous.bounding_box
            )

    return False


def detect_mouse_motion(current_frame_path, previous_frame_path):
    """
    Mouse Motion detect

    Args:
        current_frame_path ex: ./data/raw_videos/video_camera_20220422_162801-opencv/frame0:04:48.00.jpg
        previous_frame_path ex: ./data/raw_videos/video_camera_20220422_162801-opencv/frame0:04:50.00.jpg
    """

    current_cap = cv2.VideoCapture(current_frame_path)
    previous_cap = cv2.VideoCapture(previous_frame_path)

    current_success, current_image = current_cap.read()
    previous_success, previous_image = previous_cap.read()
    # image = cv2.flip(image, 1)
    # Convert the image from BGR to RGB as required by the TFLite model.
    current_rgb_image = cv2.cvtColor(current_image, cv2.COLOR_BGR2RGB)
    previous_rgb_image = cv2.cvtColor(previous_image, cv2.COLOR_BGR2RGB)
    # Create a TensorImage object from the RGB image.
    current_input_tensor = vision.TensorImage.create_from_array(
        current_rgb_image)
    previous_input_tensor = vision.TensorImage.create_from_array(
        previous_rgb_image)
    # Run object detection estimation using the model.
    current_detection_result = detector.detect(current_input_tensor)
    previous_detection_result = detector.detect(previous_input_tensor)

    print('current detection_result...')
    print(f'{current_detection_result.detections}\n')
    for index, element in enumerate(current_detection_result.detections):
        print(f'result[{index}]')
        print(f'Categories: {element.categories}')
        print(f'bounding_box: {element.bounding_box}\n')

    print('previous detection_result...')
    print(f'{previous_detection_result.detections}\n')
    for index, element in enumerate(previous_detection_result.detections):
        print(f'result[{index}]')
        print(f'Categories: {element.categories}')
        print(f'bounding_box: {element.bounding_box}\n')

    # # Draw keypoints and edges on input image
    # current_image = utils.visualize(current_image, current_detection_result)
    # previous_image = utils.visualize(previous_image, previous_detection_result)

    # cv2.imwrite('')

    return detect_algo(
        current_detection_result.detections,
        previous_detection_result.detections
    )


def test():
    """Test function"""
    test_result = detect_mouse_motion(
        '../data/raw_videos/video_camera_20220422_162801-opencv/frame0:02:10.00.jpg',
        '../data/raw_videos/video_camera_20220422_162801-opencv/frame0:02:11.00.jpg')

    print(f"test_result: {test_result}")


if __name__ == "__main__":
    test()
