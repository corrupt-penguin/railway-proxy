import requests


def app(environ, start_response):
    print(environ)
    wsgi_input = environ.get("wsgi.input")
    req_data = None
    if wsgi_input:
        req_data = wsgi_input.read()
    req_headers = {}
    for k, v in environ.items():
        if k[:5] == "HTTP_":
            req_headers[k[5:]] = v
    req = requests.Request(
        environ.get("REQUEST_METHOD"),
        environ.get("REQUEST_URI").split("?", 1)[1],
        data=req_data,
        headers=req_headers,
    )
    s = requests.Session()
    res = s.send(req.prepare())
    data = res.content
    status = "{} {}".format(res.status_code, res.reason)
    start_response(status, res.headers)
    return [data]
