import os
from utils import *

class FileExplorer: # Automatically adds file extension to the paths
    def getFunctionContent(self, path: str) -> str:
        with open(path + (".flowmc" if not path.endswith(".mcfunction") else ""), "r") as file:
            return file.read()

    def createFunctionFile(self, path: str, content: str) -> None:
        file = open(path + ".mcfunction", "w")
        file.write(content)
        file.close()

    def createSubFunctionFile(self, rootPath: str, functionName: str, content: str, index: int) -> None:
        os.makedirs(rootPath + "/" + functionName, exist_ok=True)
        self.createFunction(rootPath + "/" + functionName + "/" + indexToUUID(index), content)

EXPLORER = FileExplorer()

class SubFunction:
    def __init__(self, path, namespace, UUID):
        self.path = path
        self.UUID = UUID
        self.namespace = namespace
        self.content = ""
    
    def addLine(self,line):
        if line != "": self.content += "\n"+line
    
    def addSubFunctionReference(self,subFunctionUUID):
        self.addLine(f'function { self.namespace }:{ self.path }/{subFunctionUUID}')

    def createFile(self):
        EXPLORER.createSubFunctionFile(self.path, self.subFunctionName)
    
    def reset(self):
        content = ""


    

# Turns custom function to actual code

def format(srcPath, targetPath, namespace="test"):
    # Set up
    os.makedirs(os.path.dirname(targetPath), exist_ok=True) # creates the path to the final mcfunction files
    content = EXPLORER.getFunctionContent(srcPath).split("\n")

    # Loop variables
    knownLabels = {} # {labelName : corresponding subfunc path}. ig : {"firstlabel" : "" , "secondlabel": "/0"...}
    FUNCTION_NAME = srcPath.split("/")[-1]


    EXPLORER.createFunctionFile(f'{ targetPath }/{ FUNCTION_NAME }',
    f'function { namespace }:{ FUNCTION_NAME }/{indexToUUID(0)}')
    
    currentFunction = SubFunction(targetPath, namespace, indexToUUID(0))

    for lineNumber, line in enumerate(content):
        if line.startswith("label"):
            labelName = line [6:]
            knownLabels.update({labelName : (UUID := indexToUUID(len(knownLabels)))})

            if currentFunction.content != "":
                currentFunction.addSubFunctionReference(UUID)          
            currentFunction.reset()


        elif line.startswith("goto"):
            targetLabelName = line[5:]

        else:
            if line != "": currentChunk += "\n"+line

format("./examples/myfunction","./examples/result")
