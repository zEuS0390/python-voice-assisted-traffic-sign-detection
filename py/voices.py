import os, glob, py.database, py.util

class Voices(py.database.trafficRecoDB):

    def __init__(self, conf, voices_path, dbpath):
        super(Voices, self).__init__(dbpath)
        self.voices = {}
        self.voices_path = self.loadAudioFiles(voices_path)
        self.req = py.util.loadReq(conf)
        self.setupReq()

    # Set up the requirements
    def setupReq(self):
        self.langs = {"en":"english", "fil": "filipino"}
        self.genders = ["male", "female"]
        for lang in self.langs:
            self.insert("lang_gen_voices", lang_name=lang)
        for gender in self.genders:
            self.insert("genders", gender_name=gender)
        with open(self.req["names"], "r") as file:
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
                    print(f"[SUCCESS]: {voice_file_path} INSERTED")
                    self.insert("voice_files", voice_file_name=container["voice_file_name"],
                                                file_path=container["file_path"],
                                                file_num=container["file_num"],
                                                lang_name=container["lang_name"],
                                                gender_name=container["gender_name"],
                                                class_name=container["class_name"])
            except Exception as error:
                print(f"[ERROR {error}]: {voice_file_path} NOT INSERTED")
                continue

    # Search for all audio files in a specified directory
    def loadAudioFiles(self, root):
        found = []
        files = glob.glob(os.path.join(root, "*"))
        for file in files:
            fileType = os.path.splitext(os.path.basename(file))[1]
            if fileType in [".mp3"]:
                found.append(file)
            if os.path.isdir(file):
                found += self.loadAudioFiles(file)
        return found