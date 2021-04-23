from tkinter import *

# OpenFileDialog --Opens a window that allows you to select the desired file. It uses the TK module to do so.
#                returns a list with the data selected
def OpenFileDialog():
    from tkinter import filedialog
    windowMain = Tk()
    windowMain.withdraw()
    fileName = list(filedialog.askopenfilename(multiple=True, title="Select File",
                                               filetypes=(("root files", "*.root"), ("all files", "*.*"))))
    return fileName


#
#   SelectFolder   --Opens a window that alows you to sellect a folder path by using a graphical user interface
#                  it returns a string
def SelectFolder():
    from tkinter import filedialog
    windowMain = Tk()
    windowMain.withdraw()
    saveDir = filedialog.askdirectory(
        title=" escolha o diretório onde será criada a pasta de saida do processamento")
    return saveDir

#   CreateFolder    --Creates a folder in a given directory, with a given name.
#                   CreateFolder(PathToDirectory,FolderName)
#                   returns the directory as :
#                   "PathToDirectory/FolderName"
def CreteFolder(self, Dir, foldername):
    import os
    try:
        if not isinstance(foldername, str):
            print("Folder Name isn't a string.")
        else:
            Dir = Dir + "/" + foldername
            os.makedirs(Dir)
            print(f"Directory '{Dir}' Created.")
            return Dir
    except FileExistsError:
        print(f"The file '{Dir}' already exists.")
        return Dir



#   FolderRead      --this class allows to read and show the data stored in a given folder. Its Constructor requires
#                   a path, in order to display the files in it.
#                   The class have 3 methods :
#                   FolderRead.ListFiles    ->Returns a List containing all files in the path(with extensions)
#                   FolderRead.ListDir      ->Returns a List containing the path to all files in the directory
#                   FolderRead.ListFileName ->Returns a List containing all files in the path(no extensions)

class FolderRead:

    #Constructor
    def __init__(self, path):
        self.__path = path
        self.__listFiles = None
        self.__listFileName = None
        self.__listFileDir = None
        self.__get_ItemList()

    #Fills all variables with the items in the folder
    def __get_ItemList(self):
        import os
        self.__listFiles = os.listdir(self.__path)
        self.__listFileDir = []
        self.__listFileName = []

        for item in self.__listFiles:
            filename = item.split(sep=".")
            self.__listFileName.append(filename[0])
            if self.__path[-1] != "/":
                self.__path = self.__path + "/"
            aux = self.__path + item
            self.__listFileDir.append(aux)
    # returns the filenames with extensions
    def ListFiles(self):
        return self.__listFiles
    # returns the complete file path
    def ListFileDir(self):
        return self.__listFileDir
    # returns the Filename without extension
    def ListFileName(self):
        return self.__listFileName


# MapCreator    --Creates the pixel-to-channel correlation matrix, it also includes methods to generate random noise
#               images, generates the correction "map_channel.tsv" file, that required by PETSYST TOFPET2 processing
#               program in order to assing a pixel position to each channel.
#               SIPM: KETK PA3325-WB0808
#               System : PETSYS TOFPET2 EValuation Kit
#               ASIC model: BGA
#               Connection to J1-J2 doesnt change the pin order in the final result.
class MapCreator:
    def __init__(self):
        self.__image__ = None
        self.__Header__ = "[ChannelID,X,Y]"
        self.__ChannelToPixel__ = [[0, 1, 7],
                                   [1, 1, 6],
                                   [2, 2, 4],
                                   [3, 0, 6],
                                   [4, 0, 5],
                                   [5, 3, 7],
                                   [6, 0, 4],
                                   [7, 2, 6],
                                   [8, 1, 5],
                                   [9, 3, 3],
                                   [10, 0, 7],
                                   [11, 3, 4],
                                   [12, 3, 6],
                                   [13, 2, 5],
                                   [14, 2, 7],
                                   [15, 1, 4],
                                   [16, 6, 6],
                                   [17, 7, 7],
                                   [18, 6, 7],
                                   [19, 7, 6],
                                   [20, 4, 7],
                                   [21, 4, 6],
                                   [22, 5, 6],
                                   [23, 5, 7],
                                   [24, 7, 4],
                                   [25, 7, 5],
                                   [26, 6, 4],
                                   [27, 3, 5],
                                   [28, 6, 5],
                                   [29, 5, 5],
                                   [30, 5, 4],
                                   [31, 4, 4],
                                   [32, 4, 5],
                                   [33, 4, 3],
                                   [34, 4, 2],
                                   [35, 5, 2],
                                   [36, 5, 3],
                                   [37, 6, 2],
                                   [38, 3, 2],
                                   [39, 6, 3],
                                   [40, 7, 2],
                                   [41, 7, 3],
                                   [42, 4, 0],
                                   [43, 4, 1],
                                   [44, 5, 0],
                                   [45, 6, 1],
                                   [46, 5, 1],
                                   [47, 6, 0],
                                   [48, 7, 0],
                                   [49, 7, 1],
                                   [50, 0, 3],
                                   [51, 3, 0],
                                   [52, 3, 1],
                                   [53, 2, 1],
                                   [54, 2, 0],
                                   [55, 1, 0],
                                   [56, 1, 1],
                                   [57, 0, 2],
                                   [58, 2, 2],
                                   [59, 1, 3],
                                   [60, 0, 0],
                                   [61, 1, 2],
                                   [62, 2, 3],
                                   [63, 0, 1], ]

    # ImageFromChannel    --This method returns a 8x8 image generated from the channel list input. Each event detected
    #                       have the information of which channel have detected himself. In order to obtain the SiPM
    #                       pixel distribution for a 8x8 SiPM we feed this function with the channel sequence of each
    #                       event.

    def ImageFromChannel(self, channel, fast=True):
        import numpy as np

        image = np.zeros([8, 8])

        if fast:
            from GIMNTools import SpeedUPFunctions
            correction = self.__ChannelToPixel__
            image = SpeedUPFunctions.GenerateImage(np.asarray(channel), np.asarray(correction), image)
        else:
            for ch in channel:
                Chan, X, Y = self.__ChannelToPixel__[ch]
                image[Y][X] += 1

        return image

    # GetMap --Returns the Channel-to-pixel map as a list, the first each line represents a channel in the following
    #        order:
    #               MAP_RETURNED[a][b]
    #                            ^  ^
    #               a -> channel number ranging from 0 to 63
    #               b -> 1 : x position
    #                    2 : y position
    #
    #         in order to get position x from the  the 8x8 SiPM matrix, when channel is 60 do:
    #         XPos = MapReturned[60][1]

    def GetMap(self):
        return self.__ChannelToPixel__

    # GenerateRandomEvents --Returns a channel list to generate an image, the channel list generated is random and
    #                       is used in order to obtain a noisy image in GenerateRandomImage()
    # a noisy 8x8 image, with the event number that you desire
    def GenerateRandomEvents(self, EventNum):
        import random
        vector = []
        for i in range(EventNum):
            vector.append(random.randint(0, 63))
        return vector

    # GenerateRandomImage --Returns a noisy 8x8 image, with the event number that you desire!
    def GenerateRandomImage(self, EventNum):
        return self.ImageFromChannel(self.GenerateRandomEvents(EventNum))

    # GenerateMapTable --generates a 'map_channel.tsv' required in order to correct the channel-sipm-position.

    def GenerateMapTable(self, Path, AllSIPM=True):
        # Generates A map'tsv' filling values to all sipm, doesnt matter if it is connected or not.
        if AllSIPM is True:
            Path = Path+"/map_channel.tsv"
            File = open(Path, "w")
            PortID, SlaveID, ChipID, ChannelID, RegionID, xi, yi, x, y, z = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

            while True:

                if ChannelID == 64:
                    ChipID += 1
                    ChannelID = 0

                RegionID = ChipID // 4
                if RegionID == 4:
                    break

                Print = f"{PortID}\t{SlaveID}\t{ChipID}\t{ChannelID}\t{RegionID}\t{self.__ChannelToPixel__[ChannelID][1]}\t{self.__ChannelToPixel__[ChannelID][2]}\t{x}\t{y}\t{z}\n"

                File.write(Print)
                print(Print)
                ChannelID += 1
            File.close()
