from py.videoInput import VideoInput
from py.imagesInput import ImagesInput
from py.cameraInput import CameraInput
from py.voices import Voices
from py.util import getDir, join
import argparse, configparser, sys

"""
    TECHNOLOGICAL INSTITUTE OF THE PHILIPPINES - QUEZON CITY
    VOICE-ASSISTED TRAFFIC SIGN RECOGNITION USING YOLO ALGORITHM [2021]
    TEAM MEMBERS:
        - BALTAZAR, ZEUS JAMES
        - BANTUAS, JUNAID
        - BASBACIO, MARTIN LORENZO
        - MARQUEZ, IAN GABRIEL
"""

root_dir = getDir(__file__)

if __name__=="__main__":
    config = configparser.ConfigParser()
    config_file_path = join(root_dir, "config.ini")
    config.read(config_file_path)
    parser = argparse.ArgumentParser()
    parser.add_argument("-cam", "--camera", action="store_true", help="Detect using internal/external camera")
    parser.add_argument("-ipcam", "--ipcamera", action="store", help="Detect using ip camera")
    parser.add_argument("-vidin", "--videoinput", action="store", help="Detect in premade video")
    parser.add_argument("-imgin", "--imginput", action="store", help="Detect all in directory")
    if len(sys.argv) > 1:
        args = parser.parse_args()
        if args.camera:
            camInput = CameraInput(config)
            camInput.detectCamera()
        elif args.ipcamera is not None:
            camInput = CameraInput(config)
            camInput.detectIPCamera(args.ipcamera)
        elif args.videoinput is not None:
            vidInput = VideoInput(config)
            vidInput.detectVideo(args.videoinput)
        elif args.imginput is not None:
            imgInput = ImagesInput(config)
            imgInput.detectImages(args.imginput)