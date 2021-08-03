from py.videoInput import VideoInput
from py.imagesInput import ImagesInput
from py.cameraInput import CameraInput
from py.voices import Voices
from py.util import getDir, join
import argparse, configparser

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
    audioDB = Voices(config)
    camInput = CameraInput(config)
    vidInput = VideoInput(config)
    imgInput = ImagesInput(config)
    parser = argparse.ArgumentParser()
    parser.add_argument("-cam", "--camera", action="store_true", help="Detect using internal/external camera")
    parser.add_argument("-ipcam", "--ipcamera", action="store", help="Detect using ip camera")
    parser.add_argument("-vidin", "--videoinput", action="store", help="Detect in premade video")
    parser.add_argument("-imgin", "--imginput", action="store", help="Detect all in directory")
    args = parser.parse_args()
    if args.camera:
        camInput.detectCamera()
    elif args.ipcamera is not None:
        camInput.detectIPCamera(args.ipcamera)
    elif args.videoinput is not None:
        vidInput.detectVideo(args.videoinput)
    elif args.imginput is not None:
        imgInput.detectImages(args.imginput)