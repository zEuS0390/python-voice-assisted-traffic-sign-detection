from py.detector import TrafficSignRecognition
from py.voices import Voices
import cv2, threading, time

class CameraInput(TrafficSignRecognition):

    def __init__(self, conf):
        super(CameraInput, self).__init__(conf)
        self.audioDB = Voices(conf)
        self.camIsOpened = True
        self.current_frame = None
        self.detected_objects = None
        self.timeState = True
        self.timeInterval = 5
        self.queue = []
        threading.Thread(target=self.timeThread).start()

    def timeThread(self):
        while self.timeState:
            for c_voice in self.queue:
                self.audioDB.playVoice(c_voice, "male")
                self.queue.remove(c_voice)

    # Detection function for thread
    def detection(self):
        while self.camIsOpened:
            if  self.current_frame is not None:
                self.detected_objects = self.OBJDetector.detect(self.current_frame, NMS=True)
                for class_id in self.detected_objects["class_ids"]:
                    class_name = self.OBJDetector.classes[class_id]
                    if class_name not in self.queue:
                        self.queue.append(class_name)

    # Detect using IP or link video stream input
    def detectIPCamera(self, link):
        try:
            capture = cv2.VideoCapture(link)
        except:
            print("ERROR!")
            return
        threading.Thread(target=self.detection).start()
        while capture.isOpened():
            ret, self.current_frame = capture.read()
            if ret:
                if self.detected_objects is not None:
                    if self.detected_objects["size"] > 0:
                        self.drawDetected(self.current_frame, self.detected_objects)
                cv2.imshow("frame", self.current_frame)
                key = cv2.waitKey(1)
                if key == 27:
                    break
            else:
                break
        self.camIsOpened = False
        capture.release()
        cv2.destroyAllWindows()

    # Detect using internal/external camera
    def detectCamera(self):
        try:
            print("Initializing video capture")
            capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            if not capture.isOpened():
                print("Internal camera not detected")
                capture.release()
                capture = cv2.VideoCapture(1, cv2.CAP_DSHOW)
                if not capture.isOpened():
                    print("External camera not detected")
                    capture.release()
                    return
                else:
                    print("External camera detected")
            else:
                print("Internal camera detected")
        except:
            print("Error initializing video capture")
            capture.release()
            return
        threading.Thread(target=self.detection).start()
        while capture.isOpened():
            ret, self.current_frame = capture.read()
            if ret:
                if self.detected_objects is not None:
                    if self.detected_objects["size"] > 0:
                        self.drawDetected(self.current_frame, self.detected_objects)
                cv2.imshow("frame", self.current_frame)
                key = cv2.waitKey(1)
                if key == 27:
                    break
            else:
                break
        self.camIsOpened = False
        capture.release()
        cv2.destroyAllWindows()