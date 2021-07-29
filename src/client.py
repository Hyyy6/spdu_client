#%%
import sys
import requests
import os
import json
import base64
import socket
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import random



names = {"pc1": 0, "pc2": 1, "box1": 2, "box2": 3}

# class 


def printHelp():
    print("Usage: './<script> outletName outletState'")
    print("or './<script> fake' to send arduino request to azure function")
    return

def request_spdu_access():
    pload = {"password" : os.environ['ARD_PASS'], }
    try:
        ret = requests.post("http://spduapi.azurewebsites.net/api/spduapi", json = pload)

        print(ret)
        print(ret.content)

        if ret.status_code != 200:
            print("Could not request access.")
            return "", ""


        reply_data_string = json.loads(ret.content)
        reply_data_json = json.loads(reply_data_string["value"])

        print(reply_data_json["ipAddress"])
        print(reply_data_json["key"])

        key_base64 = reply_data_json["key"]
        key = base64.b64decode(key_base64)
        ip = reply_data_json["ipAddress"]

        print(f"ard ip - {ip} last key - {key}")
    except:
        print("Error")

    return ip, key

def change_ard_state(name, state):
    [ip, key] = request_spdu_access()
    if not ip or not key:
        print("Could not change state.")
        return -1

    pload = {"name": name, "state": state}
    try:
        print(pload)
        msg = json.dumps(pload)
        print(f"msg length: {len(msg)}")
        print("msg content: " + msg)

        if len(msg) % 16 != 0:
            print("padding")
            block_size = 16
            msg = pad(bytes(msg, "utf-8"), block_size)
        else:
            print("no padding")
        
        IV = bytearray(os.urandom(16))
        aes = AES.new(key, AES.MODE_CBC, IV)
        print("IV: ")
        print(list(IV))
        out = aes.encrypt(msg)
        msg = out + IV
        print("Encrypted with IV:")
        print(list(msg))
        ret = requests.post("http://" + ip + ':' + "1234", data = msg)
        print(ret)
        print(ret.content)

    except Exception as err:
        print("Error " + str(err))

    return 0
    
def fake_arduino():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.connect(("8.8.8.8", 80))
    local_addr = sock.getsockname()[0]
    print(local_addr)
    # key_az = bytes("abcdefghijklmnop", "utf-8")
    key_az = bytes(os.environ['KEY_ARD'], "utf-8")
    print(key_az)
    password = os.environ['ARD_PASS']
    print(password)
    key_ard = base64.encodebytes(bytearray(os.urandom(16))).decode("utf-8")
    print("key bytes length: ", len(key_ard))
    print(key_ard)
    IV = bytearray(os.urandom(16))
    pload = {
        "password": password,
        "ipAddress": local_addr,
        "key": key_ard
    }

    print(pload)
    msg = json.dumps(pload)
    print(f"msg length: {len(msg)}")
    print("msg content: " + msg)

    if len(msg) % 16 != 0:
        print("padding")
        block_size = 16
        msg = pad(bytes(msg, "utf-8"), block_size)
    else:
        print("no padding")

    aes = AES.new(key_az, AES.MODE_CBC, IV)

    out = aes.encrypt(msg)

    print("IV: ")
    print(IV)
    msg = out + IV
    print("msg with IV: ")
    print(msg)

    ret = requests.post("http://spduapi.azurewebsites.net:80/api/spduapi", 
    # ret = requests.put("http://localhost:8071/api/spduAPI",
                        headers={"Connection": "close", "Content-Length": bytes(len(msg)), }, data = msg, timeout=10)
    print(ret)
    print(ret.content)
    ret.close()

    return 0


def main(argv):
    print(len(argv))

    if argv[0] == "fake":
        fake_arduino()
    

    if len(argv) != 2:
        printHelp()
    

    if argv[0] in names and (argv[1] == '0' or argv[1] == '1'):
        name = argv[0]
        state = argv[1]
        print(f"setting {name} to {'on' if state == '1' else 'off'}")
        change_ard_state(names[name], 1 if state == '1' else 0)

    return
    

if __name__ == "__main__":
	main(sys.argv[1:])

# %%
