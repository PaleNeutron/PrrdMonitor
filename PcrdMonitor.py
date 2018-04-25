"""
This a add on for mitmproxy
usage: mitmweb -s PcrdMonitor.py
"""
from mitmproxy import contentviews
import clr
import sys
import json

sys.path.append(".\lib")
clr.AddReference("EncryptEmulator")
from EncryptEmulator import Program
from System import Byte, Array

class PcrdDataView(contentviews.View):
    name = "pcrd"
    content_types = [
        "application/json",
        "application/vnd.api+json"
]
    def __call__(self, data, **metadata) -> contentviews.TViewResult:
        if metadata["headers"]["Content-Type"] == 'application/x-msgpack':

            json_data_string = Program.DecryptResponse(data)
        else:
            json_data_string = Program.Decrypt(data)          
        json_data = json.loads(json_data_string)
        pretty = json.dumps(json_data, sort_keys=True, indent=4, ensure_ascii=False)
        return "Decrypted Json", contentviews.format_text(pretty)


view = PcrdDataView()


def load(l):
    contentviews.add(view)


def done():
    contentviews.remove(view)

if __name__ == '__main__' :

    with open("quest_skip", 'rb') as f:
        i_b = f.read()

    body = Program.Decrypt(i_b)
    print(body)