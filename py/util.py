import os, glob

IMAGETYPES = [".jpg", ".JPG", ".jpeg", ".JPEG"]
BGR_COLORS = {
    "BLUE":             (255, 0, 0),
    "RED":              (0, 0, 255),
    "GREEN":            (0, 255, 0),
    "DARK GOLDEN ROD":  (11,134,184),
    "CHART REUSE":      (0,255,127),
    "ORANGE RED":       (0,69,255),
    "AQUA":             (255,255,),
    "MAGENTA":          (255,0,255),
    "ROYAL BLUE":       (255,105,65),
    "BISQUE":           (196,228,255),
    "CRIMSON":          (60,20,220)
}

def join(*args):
    return os.path.join(*args)

# Search files in root directory
def explore(root, subdir=False):
    found = []
    files = glob.glob(join(root, "*"))
    for file in files:
        fileType = os.path.splitext(os.path.basename(file))[1]
        if fileType in IMAGETYPES:
            found.append(file)
        if subdir and os.path.isdir(file):
            found += explore(file, subdir)
    return found

def getDir(filepath):
    return os.path.dirname(os.path.realpath(filepath))