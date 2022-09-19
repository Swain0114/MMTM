from copy import deepcopy
from math import sqrt
from google.cloud import vision

threshold = 0.04


def sort_by_vertices(points):
    """sort the vertices"""
    return points.sort(
        key=lambda point: (point.bounding_poly.normalized_vertices.x,
                           point.bounding_poly.normalized_vertices.y)
    )


def wrangling_bounding_poly(normalized_vertices):
    """format the bounding poly"""
    array_of_point = []

    for vertex in normalized_vertices:
        array_of_point.append(
            (vertex.x, vertex.y)
        )

    return array_of_point


def compute_central_point(points):
    """compute central point"""
    return {
        'x': sum(point.x for point in points)/len(points),
        'y': sum(point.y for point in points)/len(points)
    }


def localize_objects(path):
    """Localize objects in the local image.

    Args:
    path: The path to the local file.
    """

    client = vision.ImageAnnotatorClient()

    with open(path, 'rb') as image_file:
        content = image_file.read()
    image = vision.Image(content=content)

    objects = client.object_localization(
        image=image).localized_object_annotations

    print(f"raw objects {objects}")
    new_objects = []
    for obj in objects:

        new_objects.append(
            {
                'name': obj.name,
                'score': obj.score,
                'boundary_points': wrangling_bounding_poly(obj.bounding_poly.normalized_vertices),
                'central_point': compute_central_point(obj.bounding_poly.normalized_vertices)
            }
        )

    return new_objects


def filter_mouse_and_animals(detect_object):
    """Only select mouse and animals type"""
    return detect_object['name'] in ('Animal', 'Mouse')


def compute_distance(pointA, pointB):
    """Compute distance"""
    x_distance = abs(pointA['x'] - pointB['x'])
    y_distance = abs(pointA['y'] - pointB['y'])

    distance = sqrt(x_distance ** 2 + y_distance ** 2)

    return distance


def find_closest_mice(current_objects, previous_objects):
    """find the closest mice object"""
    new_current_objects = []

    print(f"current_objects: {current_objects}\n")
    print(f"previous_objects: {previous_objects}\n")

    for current_object in current_objects:
        min_distance_between_previous_object_index = 'not found'
        current_central_point_diff_distance = 999
        new_previous_objects = []
        new_current_object = deepcopy(current_object)

        for index, previous_object in enumerate(previous_objects):
            new_previous_object = deepcopy(previous_object)
            central_point_diff_distance = compute_distance(
                current_object['central_point'],
                new_previous_object['central_point']
            )
            new_previous_object['central_point_diff_distance'] = central_point_diff_distance

            new_previous_objects.append(new_previous_object)
            print(
                f"central_point_diff_distance: {central_point_diff_distance}")

            if (current_central_point_diff_distance > central_point_diff_distance):
                min_distance_between_previous_object_index = index
                current_central_point_diff_distance = central_point_diff_distance

        if (min_distance_between_previous_object_index == 'not found'):
            new_current_object['previous_objects'] = None
        else:
            new_current_object['previous_objects'] = new_previous_objects[min_distance_between_previous_object_index]
            new_current_object['current_central_point_diff_distance'] = current_central_point_diff_distance

        new_current_objects.append(new_current_object)

    return new_current_objects


def detect_mouse_motion(current_frame_path, previous_frame_path):
    """
    Mouse Motion detect

    Args: 
        current_frame_path ex: ./data/raw_videos/video_camera_20220422_162801-opencv/frame0:04:48.00.jpg
        previous_frame_path ex: ./data/raw_videos/video_camera_20220422_162801-opencv/frame0:04:50.00.jpg
    """
    current_objects = localize_objects(current_frame_path)

    mouse_and_animals_current_objects = list(
        filter(filter_mouse_and_animals, current_objects)
    )
    print(
        f"current mouse and animals objects:{mouse_and_animals_current_objects}\n")

    previous_objects = localize_objects(previous_frame_path)
    mouse_and_animals_previous_objects = list(
        filter(filter_mouse_and_animals, previous_objects))

    print(
        f"previous mouse and animals objects:{mouse_and_animals_previous_objects}\n")

    comparison_objects = find_closest_mice(
        mouse_and_animals_current_objects, mouse_and_animals_previous_objects)

    print(f"comparison object:{comparison_objects}\n")

    max_central_point_diff_distance = max(
        obj['current_central_point_diff_distance'] for obj in comparison_objects)

    print(f"max distance: {max_central_point_diff_distance}")

    if (max_central_point_diff_distance > threshold):
        return True

    return False


def test():
    """Test function"""
    test_result = detect_mouse_motion(
        './data/raw_videos/video_camera_20220422_162801-opencv/frame0:04:48.00.jpg',
        './data/raw_videos/video_camera_20220422_162801-opencv/frame0:04:50.00.jpg')

    print(f"test_result: {test_result}")


if __name__ == "__main__":
    test()
