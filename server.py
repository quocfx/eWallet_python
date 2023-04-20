from email.message import EmailMessage
from http.server import BaseHTTPRequestHandler, HTTPServer
import re
import json

# import threading
from urllib import parse
from service import merchantService


def _parse_header(content_type):
    m = EmailMessage()
    m['content-type'] = content_type
    return m.get_content_type(), m['content-type'].params


# class LocalData(object):
#     records = {}


class HTTPRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if re.search('/merchant/signup/*', self.path):
            # ctype = _parse_header(self.headers.get('content-type'))
            if self.headers.get('content-type') == 'application/json':
                length = int(self.headers.get('content-length'))
                bodyStr = self.rfile.read(length).decode('utf8')
                jsonObj = json.loads(bodyStr)
                newMerchant = merchantService.addNewMerchant(jsonObj["merchantName"], jsonObj["merchantUrl"])                
                jsonStr = json.dumps(newMerchant)
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(jsonStr.encode(encoding='utf_8'))
            else:
                self.send_response(400, "Bad Request: invalid data")
                self.end_headers()
        
        # if re.search('/api/v1/addrecord/*', self.path):
        #     ctype, pdict = _parse_header(
        #         self.headers.get('content-type'))
        #     if ctype == 'application/json':
        #         length = int(self.headers.get('content-length'))
        #         rfile_str = self.rfile.read(length).decode('utf8')
        #         data = parse.parse_qs(rfile_str, keep_blank_values=1)
        #         record_id = self.path.split('/')[-1]
        #         LocalData.records[record_id] = data
        #         print("addrecord %s: %s" % (record_id, data))
        #         # HTTP 200: ok
        #         self.send_response(200)
        #     else:
        #         # HTTP 400: bad request
        #         self.send_response(400, "Bad Request: must give data")
        else:
            # HTTP 403: forbidden
            self.send_response(403)
            self.end_headers()

    def do_GET(self):
        print("GET" + self.path)
        self.send_response(200)
        # if re.search('/api/v1/shutdown', self.path):
        #     # Must shutdown in another thread or we'll hang
        #     def kill_me_please():
        #         self.server.shutdown()
        #     threading.Thread(target=kill_me_please).start()

        #     # Send out a 200 before we go
        #     self.send_response(200)
        # elif re.search('/api/v1/getrecord/*', self.path):
        #     record_id = self.path.split('/')[-1]
        #     if record_id in LocalData.records:
        #         self.send_response(200)
        #         self.send_header('Content-Type', 'application/json')
        #         self.end_headers()
        #         # Return json, even though it came in as POST URL params
        #         data = json.dumps(LocalData.records[record_id])
        #         print("getrecord %s: %s" % (record_id, data))
        #         self.wfile.write(data.encode('utf8'))
        #     else:
        #         self.send_response(404, 'Not Found: record does not exist')
        # else:
        #     self.send_response(403)

        self.end_headers()


def main():    
    server = HTTPServer(("localhost", 8080), HTTPRequestHandler)
    print('HTTP Server Running...........')
    server.serve_forever()


if __name__ == '__main__':
    main()
