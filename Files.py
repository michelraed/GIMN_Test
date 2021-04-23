from GIMNTools import Read, Utils
from GIMNTools.Read import RootDataFrame
import uproot3
import sys
import time


def ProcessGate ():
    File = Utils.OpenFileDialog()
    File=File[0]
    
    if sys.platform == 'win32':
        File=File.replace("/","\\")


    Gate = RootDataFrame(File,"gate")
    return Gate.GetData()


if __name__ == "__main__":
    t1 = time.time()
    Gate = ProcessGate()
    t2 = time.time()
    print(type(Gate))


    print('o tempo foi de {} segundos'.format(t2-t1))

    a = input("coloque algo")
    for key, values in Gate.items():
        print(key)