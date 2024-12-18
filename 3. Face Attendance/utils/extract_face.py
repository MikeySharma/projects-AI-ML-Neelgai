import cv2
import os
import tqdm
from dnn_face_detection import detect_face
import numpy as np

# Paths for video and image directories
video_path = "../dataset/video"
destination = "../dataset/images"

# Ensure the parent directory for images exists
if not os.path.exists(destination):
    os.makedirs(destination)

# Function to randomly decide with a binomial distribution
def rand():
    return np.random.binomial(n=1, p=0.2)

# Function to generate a random index within the range
def random_num(max_index):
    return int(np.random.randint(0, max_index))

# Iterate over all videos in the directory
for root, _, videos in tqdm.tqdm(os.walk(video_path)):
    for video in videos:
        video_id = os.path.basename(root)  # Correctly extract the folder name
        destination_path = os.path.join(destination, video_id)

        # Create destination folder if it doesn't exist
        if not os.path.exists(destination_path):
            os.makedirs(destination_path)

        video_file_path = os.path.join(root, video)
        cap = cv2.VideoCapture(video_file_path)

        balance = []  # For storing cropped faces
        balance_count = 0  # Count of saved images

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Flip the frame for processing
            frame = cv2.flip(frame, 1)

            # Detect faces in the frame
            faces = detect_face(frame)
            for bounding_box in faces:
                x, y, x2, y2 = map(int, bounding_box)

                # Crop and resize the face
                crop_face = frame[y:y2, x:x2]
                crop_face = cv2.resize(crop_face, (160, 160))

                # Save the cropped face
                cv2.imwrite(f"{destination_path}/{balance_count}.png", crop_face)
                balance.append(crop_face)
                balance_count += 1

        # Balance the dataset by adding synthetic images if necessary
        while balance_count < 1000:
            if rand():
                index = random_num(len(balance))
                balance_count += 1
                cv2.imwrite(f"{destination_path}/{balance_count}.png", balance[index])

        # Release video capture object
        cap.release()

print("Face extraction completed!")
