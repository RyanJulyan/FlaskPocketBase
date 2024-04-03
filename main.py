import os

# Import Monkey module from gevent for monkey-patching
from gevent import monkey

# Monkey-patching standart Python library for async working
monkey.patch_all()

# Import Compress module from Flask-Compress for compress static content (HTML, CSS, JS)
from flask_compress import Compress

# Get the WSGI server
from gevent.pywsgi import WSGIServer

from app.core.app_builder import build_app

app = build_app(health_check_kwargs={"dynamic_health_check_kwargs": "working"})

if __name__ == "__main__":
    if os.environ.get("live"):
        host = "0.0.0.0"
        port = 81

        # Create WSGI server with params for Repl.it (IP 0.0.0.0, port 8080) for our Flask app
        # To limit amount of sockets, add parameter called pool=pool and define before with pool = Pool(10000)
        http_server = WSGIServer((host, port), app)

        # Start WSGI server
        http_server.serve_forever()
    else:
        app.run(host="0.0.0.0", port=5000, debug=True)
