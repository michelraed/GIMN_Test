import uproot3
import pandas as pd
from GIMNTools import SpeedUPFunctions
import _thread
#ProcessAsDict     --Transforms the Data-structure into a Dictionary, that allows to save the data as a *.matFile
def ProcessAsDict(Acquisition: dict):
    mat_file = {}
    if isinstance(Acquisition, dict):
        mat_file["name"] = Acquisition["name"]
        mat_file["data"] = {}
        mat_file["img"] = {}
        for key, value in Acquisition["data"].items():
            mat_file["data"][key] = {}
            mat_file["data"][key]["time"] = value.time()
            mat_file["data"][key]["energy"] = value.energy()
            mat_file["data"][key]["channel"] = value.channel()
            mat_file["img"][key] = value.img()

    return mat_file


#ReadMat(filename) - Reads the "*.mat" file
def ReadMat(path):
    from scipy.io import loadmat
    Mat = loadmat(path, simplify_cells=True)
    return Mat



# RootDataFrame(RootFilePath,AqdType)--This class uses uproot to open the files with ease, it will check wich tipe
#                                   of acquisition is it we will have two options, "petsys" and "gate"
#
#                                   - petsys option is used to process petsys output and returns a dataframe
#                                   containing all data from the AQD.
#
#                                   - gate option will separate the data into singles, hits and coincidences.
#                                   AllData will be returned as a pandas Dataframe

class RootDataFrame:

    # constructor
    def __init__(self, Path: str, AqdType='petsys'):
        # initialize variables
        self.__Path = Path;
        self.__Singles = None
        self.__Raw = None
        self.__Coincidences = None
        self.__Group = None
        self.__Name = None
        self.__Gate = None

        # check if its a root file
        if self.__Path.find(".root") == -1:
            print(self.__Path)
            print("the file is not a root one")

        else:

            # opens the root file:
            self.__Data = uproot3.open(Path)

            if AqdType == "petsys":

                # stores the dataframe into the encapsulated variables __singles __raw ... etc

                if self.__Path.find("single") != -1:
                    self.__Singles = self.__Data['data'].pandas.df().to_records()
                    self.__Singles = pd.DataFrame(self.__Singles)
                    self.__Name = "single"

                elif self.__Path.find("raw") != -1:
                    self.__Raw = self.__Data['data'].pandas.df().to_records()
                    self.__Raw = pd.DataFrame(self.__Raw)
                    self.__Name = "raw"

                elif self.__Path.find("group") != -1:
                    self.__Group = self.__Data['data'].pandas.df().to_records()
                    self.__Group = pd.DataFrame(self.__Group)
                    self.__Name = "group"

                elif self.__Path.find("coincidences") != -1:
                    self.__Coincidences = self.__Data['data'].pandas.df().to_records()
                    self.__Coincidences = pd.DataFrame(self.__Coincidences)
                    self.__Name = "coincidences"

            elif AqdType == "gate":
                self.__Gate = {}

                try:
                    self.__Gate['Singles'] = pd.DataFrame(SpeedUPFunctions.GateSingles(self.__Data))
                except:
                    print("File does not contain Singles")
                try:
                    self.__Gate['Coincidences'] =pd.DataFrame(SpeedUPFunctions.GateCoincidences(self.__Data))
                except:
                    print("File does not contain Coincidences")

                try:
                    self.__Gate['Hits']=pd.DataFrame(SpeedUPFunctions.GateHits(self.__Data))
                except:
                    print("File does not contain Hits")


    # Returns data read.
    def GetData(self, verbose=False):
        if self.__Name == "single":
            if verbose:
                print("returning singles")
            return self.__Singles

        elif self.__Name == "raw":
            if verbose:
                print("returning raw")
            return self.__Raw

        elif self.__Name == "group":
            if verbose:
                print("returning group")
            return self.__Group

        elif self.__Name == "coincidences":
            if verbose:
                print("returning coincidences")
            return self.__Coincidences

        elif self.__Gate != None:
            if verbose:
                print("returning Gate")
            return self.__Gate


#   AQDStructure -This object contains the structure for the basic output from PETSYS System, have the informations
#                about this informations:
#                Asic : Represents the chipID number from the event
#                energy: event energy
#                time: time when the event was detected in pico seconds
#                channel : channel who detected the event
#                IMG: 8x8 matrix representing the counts in each channel


class AQDStructure:
    def __init__(self):
        self.__ASIC = None
        self.__energy = None
        self.__time = None
        self.__channel = None
        self.__IMG = None
        self.help = """
            The following Structure concerns the following parameter options:
            i.e : OBJECT_NAME.ASIC() | OBJECT_NAME.energy() etc..

            ASIC -> sets the ASIC number
            energy -> All events recorded in a given ASIC
            channel-> Channel occurrence of the given event
            img-> All events image

                        """

    # ASIC  --retunrs what's stored in asic
    def ASIC(self):
        return self.__ASIC

    # energy --returns whats stored in energy
    def energy(self):
        return self.__energy

    # time --returns whats stored
    def time(self):
        return self.__time

    # channel --returns whats stored
    def channel(self):
        return self.__channel

    # img --returns whats stored in the variable __IMG
    def img(self):
        return self.__IMG

    # set_Asic -- Sets the value of the variable __ASIC
    def set_ASIC(self, ASIC):
        self.__ASIC = ASIC

    # set_energy -- Sets the value of the variable __energy
    def set_energy(self, energy):
        self.__energy = energy

    # set_time -- Sets the the value of the variable __time
    def set_time(self, time):
        self.__time = time

    # set_chennel -- Sets the value of the variable __channel
    def set_channel(self, channel):
        self.__channel = channel

    # set_img   -- Generates the 8x8 SiPM map from the events distribution
    def set_img(self):
        from GIMNTools.Utils import MapCreator
        SIPMMap = MapCreator()
        if self.__channel is not None and len(self.__channel) > 1:
            self.__IMG = SIPMMap.ImageFromChannel(self.__channel)
        else:
            print("Sem informação para gerar a imagem")


# GIMNPETSingles -- This Class reads the RootFile from petsys acquisition and stores it into a data structure to
#                   manipulate the data in a python enviroment.
#                   ex: file : "myfile.root"
#                   MyAqd = GIMNPETSingles("myfile.root").GetAquisition()
#                   ChipID1 = MyAqd['data']['chipID1]
#                   ChipID1.energy() -> Gets Energy vector
#

class GIMNPETSingles:
    def __init__(self, Path):
        self.__Path = Path
        self.__Data = uproot3.open(self.__Path)
        self.__Data = self.__Data['data'].pandas.df().to_records()
        self.__AqcuisitionRaw = self.ProcessAQD()

    # ProcessAQD  --This method will generate a dictionary containing the data collected it is separated as follows:
    #             Acquisition['name'] -> Gives the name of the File Opened
    #             AQD = Acquisition['data'] -> A dictionary that separates each chipID
    #             AQD['ChipID1'] -> inside each chipID there is a data structure that stores the following data:
    #
    #             * Asic : Represents the chipID number from the event
    #             * energy: event energy
    #             * time: time when the event was detected in pico seconds
    #             * channel : channel who detected the event
    #             * IMG: 8x8 matrix representing the counts in each channel
    #

    def ProcessAQD(self, eWindow=False, eLow=0.0, eHigh=0.0):
        Df = self.__Data.copy()  # copies the dataframe
        Df["ASIC"] = Df["channelID"] // 64  # Defines the ASIC Number
        Asics = Df["ASIC"].unique()  # check how many Asics are connected
        Processed = {}  # creates the dictionaries
        Acquisition = {}

        # splits the name in order to obtain the filename
        name = self.__Path.split(sep="/")
        name = name[-1]
        name = name.split(sep=".")
        name = name[0]

        # iterates throught all SiPM separating the data from one SiPM to another
        for asic in Asics:
            if eWindow:
                Auxiliary_Dataframe = Df[
                    (Df["ASIC"] == asic) and ((Df["energy"] > eLow) & (Df["energy"] < eHigh))].copy()
            else:
                Auxiliary_Dataframe = Df[(Df["ASIC"] == asic)].copy()

            # Generates the data structure containing the data vectors
            Aqd = AQDStructure()
            Aqd.set_ASIC(f"chipID[{asic}]")
            Aqd.set_energy(Auxiliary_Dataframe["energy"])
            Aqd.set_time(Auxiliary_Dataframe["time"])
            Auxiliary_Dataframe["Channel"] = Auxiliary_Dataframe["channelID"] - (Auxiliary_Dataframe["ASIC"] * 64)
            Aqd.set_channel(Auxiliary_Dataframe["Channel"])
            Aqd.set_img()
            title = f"ChipID{asic}"
            Processed[title] = Aqd

        Acquisition["name"] = name
        Acquisition["data"] = Processed

        return Acquisition

    # Process the Acquisition to transform it To a dictionary
    def GetAcquisition(self):
        return self.__AqcuisitionRaw


# GIMNPETGroup -- This Class reads the RootFile from petsys acquisition and stores it into a data structure to
#                   manipulate the data in a python environment.
#                   ex: file : "myfile.root"
#                   MyAqd = GIMNPETSingles("myfile.root").GetAcquisition()
#                   ChipID1 = MyAqd['data']['chipID1]
#                   ChipID1.energy() -> Gets Energy vector
#

class GIIMNPETGroup:
    def __init__(self, Path):
        self.__Path = Path
        self.__Data = uproot3.open(self.__Path)
        self.__Data = self.__Data['data'].pandas.df().to_records()
        self.__AqcuisitionRaw = self.ProcessAQD()

    # ProcessAQD  --This method will generate a dictionary containing the data collected it is separated as follows:
    #             Acquisition['name'] -> Gives the name of the File Opened
    #             AQD = Acquisition['data'] -> A dictionary that separates each chipID
    #             AQD['ChipID1'] -> inside each chipID there is a data structure that stores the following data:
    #
    #             * Asic : Represents the chipID number from the event
    #             * energy: event energy
    #             * time: time when the event was detected in pico seconds
    #             * channel : channel who detected the event
    #             * IMG: 8x8 matrix representing the counts in each channel
    #

    def ProcessAQD(self, eWindow=False, eLow=0.0, eHigh=0.0):
        Df = self.__Data.copy()  # copies the dataframe
        Df["ASIC"] = Df["channelID"] // 64  # Defines the ASIC Number
        Asics = Df["ASIC"].unique()  # check how many Asics are connected
        Processed = {}  # creates the dictionaries
        Acquisition = {}

        # splits the name in order to obtain the filename
        name = self.__Path.split(sep="/")
        name = name[-1]
        name = name.split(sep=".")
        name = name[0]

        # iterates throught all SiPM separating the data from one SiPM to another
        for asic in Asics:
            if eWindow:
                Auxiliary_Dataframe = Df[
                    (Df["ASIC"] == asic) and ((Df["energy"] > eLow) & (Df["energy"] < eHigh))].copy()
            else:
                Auxiliary_Dataframe = Df[(Df["ASIC"] == asic)].copy()

            # Generates the data structure containing the data vectors
            Aqd = AQDStructure()
            Aqd.set_ASIC(f"chipID[{asic}]")
            Aqd.set_energy(Auxiliary_Dataframe["energy"])
            Aqd.set_time(Auxiliary_Dataframe["time"])
            Auxiliary_Dataframe["Channel"] = Auxiliary_Dataframe["channelID"] - (Auxiliary_Dataframe["ASIC"] * 64)
            Aqd.set_channel(Auxiliary_Dataframe["Channel"])
            Aqd.set_img()
            title = f"ChipID{asic}"
            Processed[title] = Aqd

        Acquisition["name"] = name
        Acquisition["data"] = Processed

        return Acquisition

    # Process the Acquisition to transform it To a dictionary

    def GetAcquisition(self):
        return self.__AqcuisitionRaw
