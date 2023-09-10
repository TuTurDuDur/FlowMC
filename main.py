import os
from utils import *

class FileExplorer:
    def getFunctionContent(self, path: str) -> str:
        with open(path + (".mcfunction" if not path.endswith(".mcfunction") else ""), "r") as file:
            return file.read()

    def createFunction(self, path: str, content: str) -> None:
        file = open(path + ".mcfunction", "w")
        file.write(content)
        file.close()

    def createSubFunction(self, rootPath: str, content: str, index: str) -> None:
        self.createFunction(rootPath + "/" + indexToUUID(index), content)

explorer = FileExplorer()

# Turns custom function to actual code
def format(srcPath, namespace):
    targetPath = "./result/" + srcPath
    os.makedirs(os.path.dirname(targetPath), exist_ok=True)

    content = explorer.getFunctionContent(srcPath)

    currentChunk = ""

    for line in content:
        if line.startswith("label"):
            currentChunk.append(f"function {namespace}:{}")
