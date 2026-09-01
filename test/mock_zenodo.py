#!/usr/bin/env python3
"""A stand-in Zenodo deposition API, so zenodo_stage.sh can be exercised
against the dangerous cases without touching a DOI-reserved record.

  python3 test/mock_zenodo.py --port 8899 --id-stable

--id-stable reproduces the case that made the previous script unsafe: a PUT to
an existing bucket key REPLACES the bytes but KEEPS the file id, so deleting
the id recorded before the upload destroys the new file.
"""
import argparse, hashlib, json, threading
from http.server import BaseHTTPRequestHandler, HTTPServer

ap = argparse.ArgumentParser()
ap.add_argument('--port', type=int, default=8899)
ap.add_argument('--id-stable', action='store_true')
ap.add_argument('--publish-midrun', action='store_true')
ap.add_argument('--corrupt-upload', action='store_true')
A = ap.parse_args()

STATE = {
    'submitted': False,
    'metadata': {'prereserve_doi': {'doi': '10.5281/zenodo.22236690'}},
    'files': [{'id': 'old-pdf-id', 'filename': 'Vinci_Technical_Report_No_2.pdf',
               'checksum': 'fc68060eea31eda44fc54d1631144af4', 'filesize': 230283}],
    'gets': 0,
}
NEXT = [1]

def dep(port):
    return {'state': 'unsubmitted' if not STATE['submitted'] else 'done',
            'submitted': STATE['submitted'],
            'metadata': STATE['metadata'],
            'files': STATE['files'],
            'links': {'bucket': f'http://127.0.0.1:{port}/bucket'}}

class H(BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    def _send(self, code, obj):
        b = json.dumps(obj).encode()
        self.send_response(code); self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(b))); self.end_headers(); self.wfile.write(b)

    def do_GET(self):
        STATE['gets'] += 1
        if A.publish_midrun and STATE['gets'] == 2:
            STATE['submitted'] = True          # published between upload and delete
        self._send(200, dep(A.port))

    def do_PUT(self):
        n = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(n)
        if self.path.startswith('/bucket/'):
            name = self.path.rsplit('/', 1)[-1]
            digest = hashlib.md5(body).hexdigest()
            if A.corrupt_upload: digest = '0'*32
            existing = next((f for f in STATE['files'] if f['filename'] == name), None)
            if existing:
                existing['checksum'] = digest; existing['filesize'] = len(body)
                if not A.id_stable:
                    existing['id'] = f'new-id-{NEXT[0]}'; NEXT[0] += 1
                fid = existing['id']
            else:
                fid = f'new-id-{NEXT[0]}'; NEXT[0] += 1
                STATE['files'].append({'id': fid, 'filename': name,
                                       'checksum': digest, 'filesize': len(body)})
            return self._send(201, {'key': name, 'checksum': f'md5:{digest}'})
        STATE['metadata'].update(json.loads(body or b'{}').get('metadata', {}))
        return self._send(200, dep(A.port))

    def do_DELETE(self):
        fid = self.path.rsplit('/', 1)[-1]
        before = len(STATE['files'])
        STATE['files'] = [f for f in STATE['files'] if f['id'] != fid]
        return self._send(204 if len(STATE['files']) < before else 404, {})

srv = HTTPServer(('127.0.0.1', A.port), H)
threading.Thread(target=srv.serve_forever, daemon=True).start()
print(f'mock on {A.port} id_stable={A.id_stable} publish_midrun={A.publish_midrun} corrupt={A.corrupt_upload}', flush=True)
try:
    while True: threading.Event().wait(1)
except KeyboardInterrupt:
    pass
