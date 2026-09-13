import os, json, urllib.request, urllib.error
from http.server import BaseHTTPRequestHandler, HTTPServer
BRIDGE=os.getenv('BRIDGE_URL','').rstrip('/')
HERMES=os.getenv('HERMES_URL','').rstrip('/')
KEY=os.getenv('API_KEY','')
def req(url, method='GET', headers=None, data=None):
    try:
        r=urllib.request.urlopen(urllib.request.Request(url,method=method,headers=headers or {},data=data),timeout=8)
        return r.status
    except urllib.error.HTTPError as e: return e.code
    except Exception: return 0
def scan():
    out=[]
    if BRIDGE:
        out += [{'test':'bridge_health','status':req(BRIDGE+'/healthz')}, {'test':'bridge_rejects_unauthenticated','status':req(BRIDGE+'/v1/command','POST',{'content-type':'application/json'},b'{}')}]
        if KEY: out.append({'test':'bridge_accepts_authenticated','status':req(BRIDGE+'/v1/command','POST',{'content-type':'application/json','x-api-key':KEY},b'{"command":"sentinel.check"}')})
    if HERMES: out.append({'test':'hermes_health','status':req(HERMES+'/healthz')})
    return {'agent':'atena-sentinel','mode':'defensive-allowlist','results':out}
class H(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path=='/healthz': self.send_response(200); self.end_headers(); self.wfile.write(b'{"status":"ok","agent":"atena-sentinel"}'); return
        if self.path=='/scan':
            b=json.dumps(scan()).encode(); self.send_response(200); self.send_header('content-type','application/json'); self.end_headers(); self.wfile.write(b); return
        self.send_response(404); self.end_headers()
    def log_message(self,*a): pass
HTTPServer(('0.0.0.0',int(os.getenv('PORT','3001'))),H).serve_forever()
