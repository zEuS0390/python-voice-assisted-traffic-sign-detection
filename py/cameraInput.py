from py.detector import TrafficSignRecognition
import cv2, threading

class CameraInput(TrafficSignRecognition):

    def __init__(self, conf):
        super(CameraInput, self).__init__(conf)
        self.camIsOpened = True
        self.current_frame = None
        self.detected_objects = None

    # Detection function for thread
    def detection(self):
        while self.camIsOpened:
            if  self.current_frame is not None:
                self.detected_objects = self.OBJDetector.detect(self.current_frame, NMS=True)

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