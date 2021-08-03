from py.detector import TrafficSignRecognition
from py.util import explore
import os, cv2

class ImagesInput(TrafficSignRecognition):

    def __init__(self, conf):
        super(ImagesInput, self).__init__(conf)

    # Detect in images from directory
    def detectImages(self, directory):
        newDir = os.path.join(directory, "detected_images")
        if not os.path.exists(newDir):
            os.mkdir(newDir)
        image_file_paths = explore(directory, subdir=True)
        current_no, total = 0, len(image_file_paths)
        for image_file_path in image_file_paths:
            current_no += 1
            image = cv2.imread(image_file_path)
            detected_objects = self.OBJDetector.detect(image, NMS=True)
            size = detected_objects["size"]
            image = self.drawDetected(image, detected_objects)
            if size > 0:
                cv2.imwrite(os.path.join(newDir, os.path.basename(image_file_path)), image)
                check = "detected objects" if size > 1 else "detected object"
                print(f"[SAVED][{size} detected]: {os.path.basename(image_file_path)} {size} {check} {round(current_no/total*100, 3)}% ")
            else:
                print(f"[NOT SAVED][{size} detected]: {os.path.basename(image_file_path)} ({current_no}/{total} images) {round(current_no/total*100, 3)}%")