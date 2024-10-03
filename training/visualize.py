import json
import cv2
import numpy as np
import matplotlib.pyplot as plt

# Function to project 3D points to 2D using camera intrinsics
def project_to_image(points_3d, intrinsics):
    points_3d_homogeneous = np.hstack((points_3d, np.ones((points_3d.shape[0], 1))))  # Convert to homogeneous
    points_2d = np.dot(intrinsics, points_3d_homogeneous.T).T  # Project using intrinsics
    points_2d = points_2d[:, :2] / points_2d[:, 2:]  # Normalize
    return points_2d

# Load 3D bounding box annotations from JSON
def load_annotations(annotation_file):
    with open(annotation_file, 'r') as f:
        annotations = json.load(f)
    return annotations

# Load the camera pose (extrinsics) from JSON
def load_pose(pose_file):
    with open(pose_file, 'r') as f:
        pose_data = json.load(f)
    return np.array(pose_data['camera_T_global'])

# Load camera intrinsics (assuming intrinsics are known and provided)
def load_intrinsics():
    # Example intrinsics matrix for the ring_front_center camera
    # You should replace this with actual camera calibration data if available.
    return np.array([[1400, 0, 960], 
                     [0, 1400, 540], 
                     [0, 0, 1]])

# Transform 3D bounding box from world coordinates to camera coordinates
def transform_to_camera(pose, bbox_3d):
    return np.dot(np.linalg.inv(pose), np.hstack((bbox_3d, np.ones((bbox_3d.shape[0], 1)))).T).T[:, :3]

# Function to overlay 2D bounding boxes on the image
def draw_bounding_boxes(image, points_2d):
    for i in range(4):  # Draw the front face of the bounding box
        pt1 = tuple(points_2d[i].astype(int))
        pt2 = tuple(points_2d[(i + 1) % 4].astype(int))
        cv2.line(image, pt1, pt2, (0, 255, 0), 2)
    
    for i in range(4, 8):  # Draw the back face of the bounding box
        pt1 = tuple(points_2d[i].astype(int))
        pt2 = tuple(points_2d[(i + 1) % 4 + 4].astype(int))
        cv2.line(image, pt1, pt2, (0, 255, 0), 2)
    
    # Connect the front and back faces
    for i in range(4):
        pt1 = tuple(points_2d[i].astype(int))
        pt2 = tuple(points_2d[i + 4].astype(int))
        cv2.line(image, pt1, pt2, (0, 255, 0), 2)
    return image

# Main function to overlay 2D bounding boxes on the image
def overlay_bounding_boxes(image_path, annotation_file, pose_file):
    # Load image
    image = cv2.imread(image_path)
    
    # Load annotations, pose, and camera intrinsics
    annotations = load_annotations(annotation_file)
    pose = load_pose(pose_file)
    intrinsics = load_intrinsics()

    # Iterate over each annotated object
    for annotation in annotations:
        bbox_3d = np.array(annotation['3d_bbox'])  # Assuming the 3D bounding box is in the '3d_bbox' field
        category = annotation['category']

        # Transform 3D bounding box to camera coordinates
        bbox_camera_coords = transform_to_camera(pose, bbox_3d)

        # Project 3D bounding box into 2D image coordinates
        bbox_2d = project_to_image(bbox_camera_coords, intrinsics)

        # Draw bounding box on the image
        image = draw_bounding_boxes(image, bbox_2d)

    # Display the image with bounding boxes
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.axis('off')
    plt.show()

# Example usage
image_path = "/media/william/blueicedrive/datasets/ArgoVerse/1/tracking_train1_v1.1/argoverse-tracking/train1/3d20ae25-5b29-320d-8bae-f03e9dc177b9/ring_front_center"
annotation_file = "path_to_per_sweep_annotations_amodal.json"
pose_file = "path_to_poses.json"

overlay_bounding_boxes(image_path, annotation_file, pose_file)
