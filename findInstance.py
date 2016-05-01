bret1 = open("BretzelsAndChestnuts3.in", "r")
verts = bret1.readline()
kids = bret1.readline()

for i in range(1,493):
    instance = open("phase1-processed/" + str(i) + ".in", "r")
    instanceVert = instance.readline()
    instanceKid = instance.readline()
    if verts == instanceVert and kids == instanceKid:
        print i