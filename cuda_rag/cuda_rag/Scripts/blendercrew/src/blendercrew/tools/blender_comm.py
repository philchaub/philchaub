import bpy
import json
import os
import sys

# script d'echange
def start():
    error = []
    try:
        argv = sys.argv
        for a in range(len(argv)):
            if argv[a] == "scriptPath":
                if len(argv) > a+1:
                    externalPath = argv[a+1]
                    if os.path.exists(externalPath):
                        externalText = bpy.data.texts.load(os.path.normpath(externalPath))
                        mypath, myscript = os.path.split(externalPath)
                        externalText.as_module()
    except Exception as e:
        error.append(e)
    return error


#------------------------------
error = start()

if len(error) == 0:
    error = ["no errors"]
path = "C:/Users/isisc/IA/cuda_rag/cuda_rag/Scripts/blendercrew/src/blendercrew/tools/blender_comm.json"
fileExport = os.path.normpath('{}'.format(path))
blenderMessage = {"message":["ready"],"error":error}
print("error",error)

with open(fileExport, 'w') as json_file:
    json.dump(blenderMessage, json_file, indent=4)