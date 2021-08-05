if __name__ == "__main__":
    print("This module cant be run directly.")
    exit(1)

import shlex
import asyncio


class CustomShell:
    def __init__(self,begin=">",cmdnotfound="Unknown command."):
        self._commandlist = {
            "exit":{
                "async":False,
                "func": self.exit
            }

        }
        self._begin = begin
        self._exitrequest = False
        self._uks = cmdnotfound
        pass
    def command(self,func):
        if func.__name__ in self._commandlist:
            raise TypeError(f"{func.__name__} is already a command")
        self._commandlist[func.__name__] = {
            "func": func,
            "async": asyncio.iscoroutinefunction(func)
        }
    
    def exit(self):
        self._exitrequest = True
    async def run(self):
        while not self._exitrequest:
            print(self._begin,end=" ",flush=True)
            try:
                strin = shlex.split(input())
                if strin[0] not in self._commandlist:
                    print(self._uks,flush=True)
                    continue
                if self._commandlist[strin[0]]["async"]:
                    await self._commandlist[strin[0]]["func"](*strin[1::])
                else:
                    self._commandlist[strin[0]]["func"](*strin[1::])
            except KeyboardInterrupt:
                self.exit()
            except Exception as e:
                print(e)
