import requests
import base64
import hashlib
import hmac
import json
import time

APP_ID='5d9ff727'
API_SECRET_KEY ='35f450045ba5828ceff7466818d876bd'

def findSongName(p_filename):
    url = "http://webqbh.xfyun.cn/v1/service/v1/qbh"
    curtime = str(int(time.time()))

    with open(p_filename,'rb') as payload:
        base64_param = b'eyJlbmdpbmVfdHlwZSI6InNtczE2ayIsImF1ZSI6InJhdyJ9'
        tt = str(base64_param,'utf-8')
        m2 = hashlib.md5()
        m2.update((API_SECRET_KEY+ curtime+ tt).encode('utf-8'))
        checksum = m2.hexdigest()

        header = {
            "X-CurTime": curtime,
            "X-Param": base64_param,
            "X-Appid": APP_ID,
            "X-CheckSum":checksum,
        }

        res = requests.post(url, headers=header,data=payload)
        result = res.content
        result = result.decode("utf-8")
        result_to_print = res.content.decode("unicode_escape")
        result = json.loads(result)
        result_to_print = json.loads(result_to_print)
        
        if len(result["data"]) > 0:
            song = result["data"][0]
            # print(result_to_print["data"][0]["song"])
            return song["song"]
        else:
            print(result)
            return ""

if __name__ == "__main__":
    findSongName('/home/admin/output_1chan.wav')
