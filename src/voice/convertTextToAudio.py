import websocket
import datetime
import hashlib
import base64
import hmac
import json
from urllib.parse import urlencode
import time
import ssl
from wsgiref.handlers import format_date_time
from datetime import datetime
from time import mktime
import _thread as thread

STATUS_FIRST_FRAME = 0
STATUS_CONTINUE_FRAME = 1
STATUS_LAST_FRAME = 2

APP_ID='5d9ff727'
API_KEY='0e2807aeec798d34d679c1fe2eef663b'
API_SECRET_KEY='72e18ea361a3f6958bcaf84f25627432'

class Ws_Param(object):
    def __init__(self, APPID, APIKey, APISecret, Text):
        self.APPID = APPID
        self.APIKey = APIKey
        self.APISecret = APISecret
        self.Text = Text

        self.CommonArgs = {"app_id": self.APPID}
        self.BusinessArgs = {"aue": "raw", "auf": "audio/L16;rate=16000", "vcn": "xiaoyan", "tte": "utf8"}
        self.Data = {"status": 2, "text": str(base64.b64encode(self.Text.encode('utf-8')), "UTF8")}

    def create_url(self):
        url = 'wss://tts-api.xfyun.cn/v2/tts'
        now = datetime.now()
        date = format_date_time(mktime(now.timetuple()))

        signature_origin = "host: " + "ws-api.xfyun.cn" + "\n"
        signature_origin += "date: " + date + "\n"
        signature_origin += "GET " + "/v2/tts " + "HTTP/1.1"
        signature_sha = hmac.new(self.APISecret.encode('utf-8'), signature_origin.encode('utf-8'),
                                 digestmod=hashlib.sha256).digest()
        signature_sha = base64.b64encode(signature_sha).decode(encoding='utf-8')

        authorization_origin = "api_key=\"%s\", algorithm=\"%s\", headers=\"%s\", signature=\"%s\"" % (
            self.APIKey, "hmac-sha256", "host date request-line", signature_sha)
        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')

        v = {
            "authorization": authorization,
            "date": date,
            "host": "ws-api.xfyun.cn"
        }

        url = url + '?' + urlencode(v)
        # print('websocket url :', url)
        return url

def textToPcm(p_text, p_pcmFile):
    PCM_FILE = p_pcmFile
    
    def on_message(ws, message):
        try:
            code = json.loads(message)["code"]
            sid = json.loads(message)["sid"]
            audio = json.loads(message)["data"]["audio"]
            audio = base64.b64decode(audio)
            if code != 0:
                errMsg = json.loads(message)["message"]
                print("sid:%s call error:%s code is:%s" % (sid, errMsg, code))
            else:
                #print(PCM_FILE)
                with open(PCM_FILE,'ab') as f:
                    f.write(audio)
        except Exception as e:
            print("receive msg,but parse exception:", e)

    def on_error(ws, error):
        # print("### error:", error)
        return

    def on_close(ws):
        return
        # print("### closed ###")

    def on_open(ws):
        def run(*args):
            intervel = 2

            d = {"common": wsParam.CommonArgs,
                "business": wsParam.BusinessArgs,
                "data": wsParam.Data,
                }
            d = json.dumps(d)
            ws.send(d)
            # wait for response from the server
            time.sleep(intervel)
            ws.close()

        thread.start_new_thread(run, ())
    
    wsParam = Ws_Param(APPID=APP_ID, APIKey=API_KEY,
                       APISecret=API_SECRET_KEY,
                       Text=p_text)
    websocket.enableTrace(False)
    wsUrl = wsParam.create_url()
    ws = websocket.WebSocketApp(wsUrl, on_message=on_message, on_error=on_error, on_close=on_close)
    ws.on_open = on_open
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})

if __name__ == "__main__":
    textToPcm("歌唱祖国", './test.pcm')
