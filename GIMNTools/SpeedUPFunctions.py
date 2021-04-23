from numba import jit
import numba



@jit(nopython=True)
def GenerateImage_xi_yi( xi,yi,size, image):
    if len(xi)==len(yi):
        for i in range (size):
            image[yi[i]][xi[i]]=image[yi[i]][xi[i]]+1

    return image

@jit(nopython=True)
def GenerateImage(channel,corretion,image):
    for ch in channel:
        Chan, X, Y = corretion[ch]
        image[Y][X] += 1
    return image


def GateSingles(UprootObject):
    Singles = UprootObject['Singles'].pandas.df().to_records()
    return Singles


def GateCoincidences(UprootObject):
    Coincidences = UprootObject['Coincidences'].pandas.df().to_records()
    return Coincidences

def GateHits(UprootObject):
    Hits = UprootObject['Hits'].pandas.df().to_records()
    return Hits

