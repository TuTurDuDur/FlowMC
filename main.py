import os
from utils import *

class FileExplorer: # Automatically adds file extension to the paths
    def getScriptContent(self, path: str) -> str:
        with open(path + (".flowmc" if not path.endswith(".mcfunction") else ""), "r") as file:
            return file.read()

    def createFunctionFile(self, path: str, content: str) -> None:
        try :
            file = open(path + ".mcfunction", "r")
            if (content:=file.read())=="": raise WtfError(f"File is already filled up : {content}")
            file.close()
        except:
            pass

        file = open(path + ".mcfunction", "w")
        file.write(content)
        file.close()

    def createSubFunctionFile(self, motherFunctionPath: str, content: str, subFunctionID: str) -> None:
        os.makedirs(motherFunctionPath, exist_ok=True)
        self.createFunctionFile(motherFunctionPath+ "/" + subFunctionID, content)

EXPLORER = FileExplorer()

class SubFunction:
    def __init__(self, path, namespace, /, UUID, motherName,):
        self.path = path
        self.UUID = UUID
        self.namespace = namespace
        self.content = ""
        self.motherName = motherName
    
    def addLine(self,line):
        if line != "": self.content += "\n"+line
    
    def addSubFunctionReference(self,subFunctionUUID):
        self.addLine(f'function { self.namespace }:{ self.path }/{subFunctionUUID}')

    def createFile(self):
        EXPLORER.createSubFunctionFile(self.path+"/"+self.motherName, self.content, self.UUID)
        self._reset()
    
    def _reset(self):
        self.content = ""


    

# Turns custom function to actual code

def compile(srcPath, targetPath,namespace="test"):
    unsureGoto = []
    # Set up
    os.makedirs(os.path.dirname(targetPath), exist_ok=True) # creates the path to the final mcfunction files
    content = EXPLORER.getScriptContent(srcPath).split("\n")

    # Loop variables
    knownLabels = {"#_start":0} # {labelName : corresponding subfunc path}. ig : {"firstlabel" : "" , "secondlabel": "/0"...}

    FUNCTION_NAME = srcPath.split("/")[-1]    
    EXPLORER.createFunctionFile(f'{ targetPath }/{ FUNCTION_NAME }',
    f'function { namespace }:{ FUNCTION_NAME }/0')


    currentFunction = SubFunction(targetPath, namespace, UUID = indexToUUID(0), motherName = FUNCTION_NAME)

    for lineNumber, line in enumerate(content):
        if line.startswith("label "):
            labelName = line [6:]
            if labelName not in knownLabels:
                UUID = indexToUUID(len(knownLabels))
                knownLabels.update({labelName : UUID})
            else:
                UUID = knownLabels[labelName]
            
            if currentFunction.content != "":
                currentFunction.addSubFunctionReference(UUID)
                currentFunction.createFile()
            currentFunction.UUID = UUID



        elif line.startswith("goto "):
            targetLabelName = line[5:]
            if targetLabelName not in knownLabels:
                UUID = indexToUUID(len(knownLabels))
                knownLabels.update({targetLabelName: UUID})
            else:
                UUID = knownLabels[targetLabelName]
                unsureGoto.append(UUID)
            currentFunction.addSubFunctionReference(UUID)
            currentFunction.createFile()

        else:
            currentFunction.addLine(line)

compile("examples/myfunction","examples/result")
