import os
from utils import *

class FileExplorer:

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
    os.makedirs(os.path.dirname(targetPath), exist_ok=True)

    content = explorer.getFunctionContent(srcPath).split("\n")

    currentChunk = ""
    currentFunctionIndex = 0
    knownLabels = []
    FUNCTION_NAME = srcPath.split("/")[-1]
    potentiallyUnmatchedGotos = {}

    labelMet = False

    for lineNumber, line in enumerate(content):
        if line.startswith("label"):
            labelName = line[6:]

            if not labelMet:
                labelMet = True
                explorer.createFunction(targetPath +"/"+ FUNCTION_NAME,currentChunk + f"\nfunction {namespace}:{FUNCTION_NAME}/{indexToUUID(0)}")
                currentChunk = ""

            if labelName in knownLabels:
                currentFunctionIndex = knownLabels.index(labelName)
            else:
                knownLabels.append(labelName)
                currentFunctionIndex = len(knownLabels)-1


            continue

        elif line.startswith("goto"):
            targetLabelName = line[4:]
            if targetLabelName in knownLabels:
                targetLabelIndex = knownLabels.index(targetLabelName)
            else:
                knownLabels.append(targetLabelName)
                targetLabelIndex = len(knownLabels)-1
                potentiallyUnmatchedGotos.update({targetLabelName : lineNumber})
            currentChunk += (f"\nfunction {namespace}:{FUNCTION_NAME}/{indexToUUID(targetLabelIndex)}")
            
            explorer.createSubFunction(targetPath, FUNCTION_NAME, currentChunk,currentFunctionIndex)
            currentChunk = ""
        else:
            currentChunk += "\n"+line

format("./examples/myfunction","./examples/result")
