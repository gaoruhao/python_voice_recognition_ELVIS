import requests
import base64
import hashlib
import hmac
import json
import time

def findSongName(p_filename):
    url = "http://webqbh.xfyun.cn/v1/service/v1/qbh"
    appid = "5d9ff727"
    secret_key = "35f450045ba5828ceff7466818d876bd"
    curtime = str(int(time.time()))

    with open('p_filename','rb') as payload:
        base64_param = b'eyJlbmdpbmVfdHlwZSI6InNtczE2ayIsImF1ZSI6InJhdyJ9'
        tt = str(base64_param,'utf-8')
        m2 = hashlib.md5()
        m2.update((secret_key+ curtime+ tt).encode('utf-8'))
        checksum = m2.hexdigest()

        header = {
            "X-CurTime": curtime,
            "X-Param": base64_param,
            "X-Appid": appid,
            "X-CheckSum":checksum,
        }

        res = requests.post(url, headers=header,data=payload)
        result = res.content
        result = result.decode("unicode_escape")
        result = json.loads(result)
        for song in result["data"]:
            print(song["song"], ", singer is ", song["singer"])

if __name__ == "__main__":
    findSongName('/home/admin/output_1chan.wav')