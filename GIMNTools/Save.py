
#SaveAsMat  --Saves the acquisition as a MatFile
def SaveAsMat(Dict, Dir):
    from scipy.io import savemat
    try:
        Name = Dict["name"]
        if Dir[-1] != "/":
            Dir = Dir + "/"
        Dir = Dir + Name + ".mat"
        savemat(Dir, Dict)
    except FileExistsError:
        print("images already exist")

