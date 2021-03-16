#%%
import sys
import requests

names = {"pc1": 0, "pc2": 1, "box1": 2, "box3": 3}



def printHelp():
    print("Usage: ./<script> outletName outletState")

def getKey():
    return
    

def main(argv):
	# for arg in argv:
	# 	print(arg)
	# print ("main")
    if argv.size() != 2:
        print("bad input")
        print_help()
    
    

if __name__ == "__main__":
	main(sys.argv[1:])

print ("hello world")
# %%
