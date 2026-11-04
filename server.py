"""Minimal zero-dependency static file server for Railway/Render.

The NKT suite is pure static HTML, so no framework is needed.
Railway injects the listening port via the $PORT environment variable.
"""

import os
from functools import partial
from http.server import HTTPServer, SimpleHTTPRequestHandler

ROOT = os.path.dirname(os.path.abspath(__file__))
PORT = int(os.environ.get("PORT", "8080"))

handler = partial(SimpleHTTPRequestHandler, directory=ROOT)
httpd = HTTPServer(("0.0.0.0", PORT), handler)
print(f"NKT Suite serving on 0.0.0.0:{PORT}", flush=True)
httpd.serve_forever()
