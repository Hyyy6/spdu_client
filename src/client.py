#%%
import sys
import requests

names = {"pc1": 0, "pc2": 1, "box1": 2, "box3": 3}

def main(argv):
	for arg in argv:
		print(arg)
	print ("main")


if __name__ == "__main__":
	main(sys.argv)

print ("hello world")
# %%
