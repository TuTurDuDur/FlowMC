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

    def createSubFunctionFile(self, path: str, content: str, subFunctionID: str) -> None:
        os.makedirs(path, exist_ok=True)
        self.createFunction(path+ "/" + subFunctionID, content)

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
        EXPLORER.createSubFunctionFile(self.path, self.content, self.UUID)
        self._reset()
    
    def _reset(self):
        self.content = ""


    

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

            UUID = indexToUUID(len(knownLabels))
            knownLabels.update({labelName : UUID})
            
            if currentFunction.content != "":
                currentFunction.addSubFunctionReference(UUID)
                currentFunction.createFile()


        elif line.startswith("goto"):
            targetLabelName = line[5:]
            if targetLabelName not in knownLabels.keys():
                UUID = indexToUUID(len(knownLabels))
                knownLabels.update({labelName: UUID})
            else:
                UUUID = knownLabels[targetLabelName]
            currentFunction.addSubFunctionReference(UUID)
            currentFunction.createFile()


        else:
            currentFunction.addLine(line)

format("./examples/myfunction","./examples/result")
