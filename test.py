
class FileExplorer():
    def getFunctionContent(self,path: str) -> str:
        with open(path + (".mcfunction" if not path.endswith(".mcfunction") else ""), "r") as file:
            return file.read()

    def createFunction(self, path: str, content: str) -> None:
        file = open(path + ".mcfunction","w")
        file.write(content)
        file.close()


    def createSubFunction(self, root_path : str, content: str, index: str) -> None:
        self.createFunction(root_path + "/" + eval(index), content)


print(FileExplorer().getFunctionContent("./examples/function"))