import os, glob

IMAGETYPES = [".jpg", ".JPG", ".jpeg", ".JPEG"]

# Search files in root directory
def explore(root, subdir=False):
    found = []
    files = glob.glob(os.path.join(root, "*"))
    for file in files:
        fileType = os.path.splitext(os.path.basename(file))[1]
        if fileType in IMAGETYPES:
            found.append(file)
        if subdir and os.path.isdir(file):
            found += explore(file, subdir)
    return found