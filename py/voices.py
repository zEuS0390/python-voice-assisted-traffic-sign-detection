from py.util import join, getDir
from py.database import trafficRecoDB
import os, glob, winsound, random

root_dir = getDir(getDir(__file__))
req_dir = join(root_dir, "req")

# file_name
# file_path
# class_name
# lang_name
# gender_name
# class_name

class GroupVoice:

    def __init__(self):
        self.femaleVoices = []
        self.maleVoices = []

    def add(self, voice):
        print(voice.file_name, voice.gender_name)
        if voice.gender_name == "female":
            self.femaleVoices.append(voice)
        elif voice.gender_name == "male":
            self.maleVoices.append(voice)

    def __repr__(self):
        return f"{self.voices}"

class Voice:

    def __init__(self, file_name, file_path,
                       file_num, lang_name,
                       gender_name, class_name):
        self.file_name = file_name
        self.file_path = file_path
        self.file_num = file_num
        self.class_name = class_name
        self.lang_name = lang_name
        self.gender_name = gender_name

    def play(self):
        winsound.PlaySound(self.file_path, winsound.SND_FILENAME)

    def __repr__(self):
        return self.file_name


class Voices(trafficRecoDB):

    def __init__(self, conf):
        super(Voices, self).__init__(conf["Requirements"]["database"]+".db")
        self.voices_path = self.loadAudioFiles(join(root_dir, conf["Requirements"]["voices_directory"]))
        self.conf = conf
        self.setupReq()
        self.removeNoExist("voice_files")
        self.insertToDB()

    def playVoice(self, class_name, gender_name):
        if gender_name == "male":
            voices = self.getVoices()[class_name].maleVoices
            random.choice(voices).play()
        elif gender_name == "female":
            voices = self.getVoices()[class_name].femaleVoices
            random.choice(voices).play()

    # Get the voices for use
    def getVoices(self):
        voices = {}
        for name in self.names:
            class_voices = self.getAllWhere("voice_files", class_Name=name)
            group_c_voices = GroupVoice()
            for c_voice in class_voices:
                file_name = c_voice[0]
                file_path = c_voice[1]
                file_num = c_voice[2]
                lang_name = c_voice[3]
                gender_name = c_voice[4]
                class_name = c_voice[5]
                group_c_voices.add(Voice(file_name, file_path, file_num,
                                         lang_name, gender_name, class_name))
            voices[name] = group_c_voices
        return voices

    # Set up the requirements
    def setupReq(self):
        self.langs = {"en":"english", "fil": "filipino"}
        self.genders = ["male", "female"]
        for lang in self.langs:
            self.insert("lang_gen_voices", lang_name=lang)
        for gender in self.genders:
            self.insert("genders", gender_name=gender)
        with open(join(req_dir, self.conf["Requirements"]["names"]), "r") as file:
            self.names = [name.rstrip() for name in file.readlines()]
            for name in self.names:
                self.insert("classes", class_name=name)

    # Get the parameters for table insertion
    def getParams(self, root):
        container = {}
        if os.path.isfile(root):
            basename = os.path.basename(root)
            filename = os.path.splitext(basename)[0]
            parameters = filename.split("_")
            if len(parameters) == 4:
                lang_name = parameters[0]
                class_name = parameters[1]
                gender_name = parameters[2].replace("(", "").replace(")", "")
                number = parameters[3]
                if lang_name in self.langs and \
                   class_name in self.names and \
                   gender_name in self.genders and \
                   number.isdigit():
                   container["voice_file_name"] = filename
                   container["file_path"] = root
                   container["file_num"] = int(number)
                   container["lang_name"] = self.langs[lang_name]
                   container["class_name"] = class_name
                   container["gender_name"] = gender_name
            else:
                return None
        return container

    # Insert audio file paths in the database
    def insertToDB(self):
        for voice_file_path in self.voices_path:
            try:
                container = self.getParams(voice_file_path)
                if container is not None:
                    print(f"[AUDIO LOAD]: {os.path.basename(voice_file_path)}")
                    self.insert("voice_files", voice_file_name=container["voice_file_name"],
                                                file_path=container["file_path"],
                                                file_num=container["file_num"],
                                                lang_name=container["lang_name"],
                                                gender_name=container["gender_name"],
                                                class_name=container["class_name"])
                else:
                    print(f"[AUDIO FAILED]: {os.path.basename(voice_file_path)}")
            except Exception as error:
                print(f"[ERROR {error}]: {voice_file_path}")
                continue

    # Search for all audio files in a specified directory
    def loadAudioFiles(self, root):
        found = []
        files = glob.glob(os.path.join(root, "*"))
        for file in files:
            fileType = os.path.splitext(os.path.basename(file))[1]
            if fileType in [".wav"]:
                found.append(file)
            if os.path.isdir(file):
                found += self.loadAudioFiles(file)
        return found

    