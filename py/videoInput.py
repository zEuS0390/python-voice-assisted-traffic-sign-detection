from os.path import join, dirname, exists, basename, realpath
from py.detector import TrafficSignRecognition
from os import mkdir
import cv2

class VideoInput(TrafficSignRecognition):

    def __init__(self, conf):
        super(VideoInput, self).__init__(conf)

    # Detect in frames from video input
    def detectVideo(self, file_path):
        newDir = join(dirname(file_path), "detected_videos")
        if not exists(newDir):
            mkdir(newDir)
        if not exists(realpath(file_path)):
            print(f"[ERROR]: {basename(file_path)} does not exist")
            return
        capVid = cv2.VideoCapture(realpath(file_path))
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        curr_frame, total_frames = 0, int(capVid.get(cv2.CAP_PROP_FRAME_COUNT))
        vidWriter = cv2.VideoWriter(join(newDir, basename(file_path)),
                                    fourcc,
                                    capVid.get(cv2.CAP_PROP_FPS),
                                    (int(capVid.get(cv2.CAP_PROP_FRAME_WIDTH)),
                                     int(capVid.get(cv2.CAP_PROP_FRAME_HEIGHT))))
        prompt = "[VIDEO SAVED]: Traffic sign detection is done."
        try:
            while capVid.isOpened():
                curr_frame += 1
                ret, frame = capVid.read()
                if ret:
                    detected_objecs = self.OBJDetector.detect(frame, NMS=True)
                    print("[FRAME][{} detected]: Detect traffic sign objects ({}/{} frames) {}% "\
                            .format(len(detected_objecs["class_ids"]), curr_frame, total_frames, round(curr_frame/total_frames*100, 3)))
                    frame = self.drawDetected(frame, detected_objecs)
                    vidWriter.write(frame)
                else:
                    break
        except KeyboardInterrupt:
            prompt = "[VIDEO SAVED]: Traffic sign detection has been stopped."
        print(prompt)
        capVid.release()
        vidWriter.release()