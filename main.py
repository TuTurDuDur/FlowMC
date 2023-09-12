import os
from utils import *

class FileExplorer: # Automatically adds file extension to the paths
    def getFunctionContent(self, path: str) -> str:
        with open(path + (".flowmc" if not path.endswith(".mcfunction") else ""), "r") as file:
            return file.read()

    def createFunction(self, path: str, content: str) -> None:

        file = open(path + ".mcfunction", "w")
        file.write(content)
        file.close()

    def createSubFunction(self, rootPath: str, functionName: str, content: str, index: int) -> None:
        os.makedirs(rootPath + "/" + functionName, exist_ok=True)
        self.createFunction(rootPath + "/" + functionName + "/" + indexToUUID(index), content)

explorer = FileExplorer()

# Turns custom function to actual code

def format(srcPath, targetPath, namespace="test"):
    # Set up
    os.makedirs(os.path.dirname(targetPath), exist_ok=True) # creates the path to the final mcfunction files
    content = explorer.getFunctionContent(srcPath).split("\n")

    # Loop variables
    currentChunk = "" # Body of the current subfunction
    knownLabels = {} # {labelName : corresponding subfun path}. ig : {"firstlabel" : "" , "secondlabel": "/0"...}
    FUNCTION_NAME = srcPath.split("/")[-1]


    explorer.createFunction(f'{ targetPath }/{ FUNCTION_NAME }',
    f'function { namespace }:{ FUNCTION_NAME }/{indexToUUID(0)}')

    for lineNumber, line in enumerate(content):
        if line.startswith("label"):
            labelName = line [6:]
            knownLabels.update({labelName : indexToUUID(len(knownLabels))})
            labelsMet += 1 
            
               

            continue

        elif line.startswith("goto"):
            pass

        else:
            if line != "": currentChunk += "\n"+line

format("./examples/myfunction","./examples/result")
