import cv2, os, py.detector

class VideoInput(py.detector.TrafficSignRecognition):

    def __init__(self, conf):
        super(VideoInput, self).__init__(conf)

    # Detect in frames from video input
    def detectVideo(self, file_path):
        newDir = os.path.join(os.path.dirname(file_path), "detected_videos")
        if not os.path.exists(newDir):
            os.mkdir(newDir)
        capVid = cv2.VideoCapture(file_path)
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        curr_frame, total_frames = 0, int(capVid.get(cv2.CAP_PROP_FRAME_COUNT))
        vidWriter = cv2.VideoWriter(os.path.join(newDir, os.path.basename(file_path)),
                                    fourcc,
                                    capVid.get(cv2.CAP_PROP_FPS),
                                    (int(capVid.get(cv2.CAP_PROP_FRAME_WIDTH)),
                                     int(capVid.get(cv2.CAP_PROP_FRAME_HEIGHT))))
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