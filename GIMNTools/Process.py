import os
#   ProcessPETSYSRaw(PETSYSSoftwarePath, Config, File, OutName, OutPath):
#    This class allows to process the rawData from Petsys into Singles, Coincidences, Raws and Groups. It uses the programs
#    and applications provided by PETSYS Electronics, and to use this class you must have PETSYS software installed.
#    The imput are 5 variables:
#
#        PETSYSSoftwarePath - Path where PETSYS Software is installed
#        Config - Path where config.ini file is located
#        File -  Raw File that you want to process
#        OutName - Name of the output File
#        OutPath - Path where the output will be saved
#
#   The values can be changed through the methods:
#
#       set_PETSYSSoftwarePath
#       set_Config
#       set_File
#       set_OutName
#       set_outPath
#
#   The values can be visualized by the methods:
#
#       PETSYSSoftwarePath
#       Config
#       File
#       OutName
#       OutPath
#


class ProcessPETSYSRaw:
    def __init__(self, PETSYSSoftwarePath, Config, File, OutName, OutPath):
        # check the possibility of use subprocess in future

        self.__PETSYSSoftwarePath = PETSYSSoftwarePath
        self.__Config = Config
        self.__File = File
        self.__OutName = OutName
        self.__OutPath = OutPath

    def Singles(self):
        Out = self.__OutPath + "/" + self.__OutName + "_single.root"
        command = "{0}./convert_raw_to_singles --config {1} -i {2} -o {3} --writeRoot"
        os.system(command.format(self.__PETSYSSoftwarePath, self.__Config, self.__File, Out))

    def Coincidence(self):
        Out = self.__OutPath + "/" + self.__OutName + "_coincidence"
        command = "{0}./convert_raw_to_coincidence --config {1} -i {2} -o {3} --writeRoot"
        os.system(command.format(self.__PETSYSSoftwarePath, self.__Config, self.__File, Out))

    def Group(self):
        Out = self.__OutPath + "/" + self.__OutName + "_group.root"
        command = "{0}./convert_raw_to_group --config {1} -i {2} -o {3} --writeRoot"
        os.system(command.format(self.__PETSYSSoftwarePath, self.__Config, self.__File, Out))

    def Raw(self):
        Out = self.__OutPath + "/" + self.__OutName + "_raw.root"
        command = "{0}./convert_raw_to_raw --config {1} -i {2} -o {3} --writeRoot"
        os.system(command.format(self.__PETSYSSoftwarePath, self.__Config, self.__File, Out))

    def set_PetsysSoftwarePath(self, PETSYSSoftwarePath):
        self.__PETSYSSoftwarePath = PETSYSSoftwarePath

    def PetsysSoftwarePath(self):
        return self.__PETSYSSoftwarePath

    def set_Config(self, config):
        self.__Config = config

    def Config(self):
        return self.__Config

    def set_File(self, File):
        self.__File = File

    def File(self):
        return self.__File

    def set_OutName(self, OutName):
        self.__OutName = OutName

    def OutName(self):
        return self.__OutName

    def set_OutPath(self, OutPath):
        self.__OutPath = OutPath

    def OutPath(self):
        return self.__OutPath