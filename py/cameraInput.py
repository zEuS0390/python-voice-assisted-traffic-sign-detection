from py.detector import TrafficSignRecognition
from py.voices import Voices
import cv2, threading, time

class counter(threading.Thread):

    def __init__(self, interval, state):
        super(counter, self).__init__()
        self.interval = interval
        self.t_s = 0
        self.state = state

class CameraInput(TrafficSignRecognition):

    def __init__(self, conf):
        super(CameraInput, self).__init__(conf)
        self.conf = conf
        self.audioDB = Voices(conf)
        self.camIsOpened = True
        self.current_frame = None
        self.detected_objects = None
        self.counterState = True
        self.voiceState = True
        self.windowTitle = "Traffic Sign Recognition for Driver's Awareness"
        interval = conf.getint("Voice", "interval")
        self.voiceOnce = {
            "stop":             counter(interval, True), # counter(<time_interval>, <readyToPlay>)
            "intersection":     counter(interval, True),
            "no u turn":        counter(interval, True),
            "no left turn":     counter(interval, True),
            "no right turn":    counter(interval, True),
            "speed limit":      counter(interval, True),
            "pedestrian":       counter(interval, True),
            "warning":          counter(interval, True),
            "no parking":       counter(interval, True),
            "one way":          counter(interval, True),
            "no entry":         counter(interval, True)
        }
        self.queue = []
        threading.Thread(target=self.counterThread).start() # Thread for the counter
        threading.Thread(target=self.voiceThread).start() # Thread for the voice output

    def counterThread(self):
        while self.counterState:
            for class_name in self.voiceOnce:
                reserved = self.voiceOnce[class_name]
                if not reserved.state:
                    if reserved.t_s < reserved.interval:
                        reserved.t_s += 1
                    else:
                        reserved.t_s = 0
                        reserved.state = True
            time.sleep(1)

    def voiceThread(self):
        while self.voiceState:
            try:
                for play in self.queue:
                    if self.voiceOnce[play].state:
                        self.audioDB.playVoice(play, self.conf["Voice"]["gender"])
                        self.voiceOnce[play].state = False
                        self.queue.remove(play)
            except Exception as exception:
                print(f"[ERROR {exception}]: No voice is being played.")
                continue
            # print(" ".join([str(self.voiceOnce[class_name].t_s) for class_name in self.voiceOnce]))

    # Detection function for thread
    def detection(self):
        while self.camIsOpened:
            if  self.current_frame is not None:
                self.detected_objects = self.OBJDetector.detect(self.current_frame, NMS=True)
                if self.detected_objects["size"] == 0:
                    self.queue.clear()
                for class_id in self.detected_objects["class_ids"]:
                    class_name = self.OBJDetector.classes[class_id]
                    if class_name not in self.queue:
                        self.queue.append(class_name)
        self.voiceState = False
        self.counterState = False

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
                cv2.imshow(self.windowTitle, self.current_frame)
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
                cv2.imshow(self.windowTitle, self.current_frame)
                key = cv2.waitKey(1)
                if key == 27:
                    break
            else:
                break
        self.camIsOpened = False
        capture.release()
        cv2.destroyAllWindows()