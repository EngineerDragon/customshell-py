if __name__ == "__main__":
    print("This module cant be run directly.")
    exit(1)

import shlex

class CustomTerminal:
    def __init__(self,begin=">",unknowncommandstr="Unknown command."):
        self._commandlist = {
            "exit":self.exit
        }
        self._begin = begin
        self._exitrequest = False
        self._uks = unknowncommandstr
        pass
    def command(self,func):
        if func.__name__ in self._commandlist:
            raise TypeError(f"{func.__name__} is already a command")
        self._commandlist[func.__name__] = func
    def exit(self):
        self._exitrequest = True
    def run(self):
        while not self._exitrequest:
            print(self._begin,end=" ")
            try:
                strin = shlex.split(input())
                if strin[0] not in self._commandlist:
                    print(self._uks)
                    continue
                self._commandlist[strin[0]](*strin[1::])
            except KeyboardInterrupt:
                self.exit()
            except Exception as e:
                print(e)