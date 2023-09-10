import os
from utils import *

class FileExplorer():
    def getFunctionContent(self,path: str) -> str:
        with open(path + (".mcfuntion" if not path.endswith(".mcfunction") else ""), "r") as file:
            return file.read()

    def createFunction(self, path: str, content: str) -> None:
        file = open(path + ".mcfunction","w")
        file.write(content)
        file.close()


    def createSubFunction(self, root_path : str, content: str, index: str) -> None:
        self.createFunction(root_path + "/" + indexToUUID(index), content)

explorer = FileExplorer()

# Turns custom function to actual code
def format(src_path,namespace):
    target_path = "./result/"+src_path
    os.makedirs(os.path.dirname(target_path), exist_ok=True)
    
    content = explorer.getFunctionContent(src_path)

    current_chunk = ""

    for line in content:
        if line.startswith("label"):
            current_chunk.append(f"function {namespace}:{}")


    






format("function")