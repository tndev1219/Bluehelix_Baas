import requests
import json
import time
from binascii import hexlify, unhexlify
import ed25519
import base64

domain     = "https://baas.bluehelix.com"
public_key = "6407b297a07c352a51ea5bccf8bf7d57c0852a482a81c8bb75386542bd3fbfc9"
private_key = "f75b4493a3e689291c92f243825170c2c30c256fdfe22ea35b5150280b6bbe92"
chain      = "BTCV-7206"
api_key     = "2e299a9e36d34bb99d7b5e50b1d8fdfe"

def get_address_count():
    timestamp = str(int(time.time() * 1000))
    path = "/api/v1/address/unused/count?chain="+chain

    sign_msg = create_sign_msg("GET", path, timestamp, {})
    sign_msg = sign_msg.encode("utf-8")

    signing_key = ed25519.SigningKey(private_key.encode("utf-8"), encoding="hex")
    signature = signing_key.sign(sign_msg)
    print("signature = ", hexlify(signature))

    headers  = {
        "BWAAS-API-KEY": api_key,
        "BWAAS-API-TIMESTAMP": timestamp,
        "BWAAS-API-SIGNATURE": hexlify(signature)
    }

    try:
        res = requests.get(url=domain+path, headers=headers)
        print('-------------------------')
        print(res.text)
        print('-------------------------')
    except ValueError:
        print('-- get_address_count error --', ValueError)


def add_address():
    timestamp = str(int(time.time() * 1000))

    data = {
        "chain": chain,
        "addr_list": [
            "BAAS-TEST-address-123456",
            "BAAS-TEST-address-654321"
        ]
    }
    sign_msg = create_sign_msg(
        "POST", "/api/v1/address/add", timestamp, data)
    sign_msg = sign_msg.encode("utf-8")

    signing_key = ed25519.SigningKey(private_key.encode("utf-8"), encoding="hex")
    signature = signing_key.sign(sign_msg)
    print("signature = ", hexlify(signature))

    headers = {
        "BWAAS-API-KEY": api_key,
        "BWAAS-API-TIMESTAMP": timestamp,
        "BWAAS-API-SIGNATURE": hexlify(signature),
        "Content-Type": "application/json"
    }

    try:
        res = requests.post(url=domain+"/api/v1/address/add", data=json.dumps(data),  headers=headers)
        print('-------------------------')
        print(res.text)
        print('-------------------------')
    except ValueError:
        print('-- add_address error --', ValueError)

    
def create_key():
    signing_key, verifying_key = ed25519.create_keypair()
    print("the private key is", signing_key.to_ascii(encoding="hex"))
    print("the public key is", verifying_key.to_ascii(encoding="hex"))


def create_sign_msg(method,url, timestamp, body):
    params_list = [method, url, timestamp]
   
    if method == "POST":
        sorted_body = sorted(body.items(),  key=lambda d: d[0], reverse=False)
        print("sorted_body= ", sorted_body)

        data_list = []
        for data in sorted_body:
            if isinstance(data[1],list):
                value = "["+" ".join(data[1])+"]"
                key = data[0]
                data_list.append(key+"="+value)
            else:
                data_list.append("=".join(data))

        body_params = "&".join(data_list)
        params_list.append(body_params)

    params_str = "|".join(params_list)
    print("params_str= ", params_str)
    return params_str
        

# create_key()
# get_address_count()
add_address()
