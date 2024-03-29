from py.util import getDir, join, BGR_COLORS
import cv2, numpy

root_dir = getDir(getDir(__file__))
req_dir = join(root_dir, "req")

# Detector class
class detector(object):

    # Requirements
    # {
    #   "weights":  <model>, 
    #   "cfg":      <configuration>, 
    #   "names":    <labels>
    #  }
    def __init__(self, conf):
        self.conf = conf
        self.loadModel()

    # Load the model
    def loadModel(self):
        self.network = cv2.dnn.readNet(join(req_dir, self.conf["Requirements"]["weights"]), 
                                       join(req_dir, self.conf["Requirements"]["cfg"]))
        if self.conf.getboolean("GPU", "CUDA"):
            self.network.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
            self.network.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
        layer_names = self.network.getLayerNames()
        self.output_layers = [layer_names[layer[0] - 1] for layer in self.network.getUnconnectedOutLayers()]
        with open(join(req_dir, self.conf["Requirements"]["names"]), "r") as file:
            self.classes = [line.rstrip() for line in file.readlines()]

    # Detection method
    def detect(self, image, NMS=False):
        if image is None:
            return
        height, width, shape = image.shape
        blob = cv2.dnn.blobFromImage(image, 1/255, 
                                    (self.conf.getint("Detection", "width"), 
                                     self.conf.getint("Detection", "height")), 
                                    swapRB=True, crop=False)
        self.network.setInput(blob)
        outputs = self.network.forward(self.output_layers)
        all_detected = {"squares": [], 
                        "confidences": [],
                        "class_ids": [],
                        "size": 0}
        for out in outputs:
            for detected in out:
                scores = detected[5:]
                class_id = numpy.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.5:
                    center_x = int(detected[0] * width)
                    center_y = int(detected[1] * height)
                    square_w = int(detected[2] * width)
                    square_h = int(detected[3] * height)
                    square_x = int(center_x - square_w / 2)
                    square_y = int(center_y - square_h / 2)
                    all_detected["squares"].append([square_x, square_y, square_w, square_h])
                    all_detected["confidences"].append(float(confidence))
                    all_detected["class_ids"].append(class_id)
                    all_detected["size"] += 1
        if NMS:
            NMSDetected = {"squares":[], "confidences":[], "class_ids":[], "size": 0}
            indices = cv2.dnn.NMSBoxes(all_detected["squares"], \
                                       all_detected["confidences"], \
                                       0.5, 0.5)
            for index in range(len(all_detected["squares"])):
                if [index] in indices:
                    NMSDetected["squares"].append(all_detected["squares"][index])
                    NMSDetected["confidences"].append(all_detected["confidences"][index])
                    NMSDetected["class_ids"].append(all_detected["class_ids"][index])
                    NMSDetected["size"] += 1
            return NMSDetected
        return all_detected

# Main class for traffic sign recognition
class TrafficSignRecognition(object):

    # Constructor
    def __init__(self, conf):
        self.OBJDetector = detector(conf)

    # Draw the image with detected object/s
    def drawDetected(self, image, detected_objects, thickness=2):
        for index in range(detected_objects["size"]):
            x_pos, y_pos, w_size, h_size = detected_objects["squares"][index]
            confidence = detected_objects["confidences"][index]
            class_id = detected_objects["class_ids"][index]
            color = BGR_COLORS[list(BGR_COLORS.keys())[class_id]]
            cv2.rectangle(image, (x_pos, y_pos), (x_pos+w_size, y_pos+h_size), color, thickness)
            cv2.putText(image, self.OBJDetector.classes[class_id]+" "+str(round(confidence, 2)), (x_pos, y_pos), cv2.FONT_HERSHEY_PLAIN, 2, color, thickness)
        return image