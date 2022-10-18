import requests


def app(environ, start_response):
    wsgi_input = environ.get("wsgi.input")
    req_data = None
    if wsgi_input:
        req_data = wsgi_input.read()
    req_headers = {}
    for k, v in environ.items():
        if k[:5] == "HTTP_":
            req_headers[k[5:]] = v
    host = ""
    if "HOST" in req_headers:
        host = req_headers.pop("HOST")
    url = environ.get("RAW_URI")
    if url[:3] == "/r/":
        url = url[3:]
        req_headers["X_FORWARDED_FOR"] = environ.get("REMOTE_ADDR")
    else:
        url = url[1:]
    req = requests.Request(
        environ.get("REQUEST_METHOD"),
        url,
        data=req_data,
        headers=req_headers,
    )
    s = requests.Session()
    res = s.send(req.prepare())
    if "text/html" in res.headers.get("Content-Type"):
        host_url = "{}://{}/".format(environ.get("wsgi.url_scheme").replace("t", "x"), host)
        html = res.text
        html = html.replace("href=\"https://", "href=\"" + host_url + "https://")
        html = html.replace("href=\"http://", "href=\"" + host_url + "http://")
        html = html.replace("href=\"//", "href=\"" + host_url + url.split(":")[0] + "://")
        html = html.replace("href=\"/", "href=\"" + host_url + "/".join(url.split("/")[:3]) + "/")
        html = html.replace("href='https://", "href='" + host_url + "https://")
        html = html.replace("href='http://", "href='" + host_url + "http://")
        html = html.replace("href='//", "href='" + host_url + url.split(":")[0] + "://")
        html = html.replace("href='/", "href='" + host_url + "/".join(url.split("/")[:3]) + "/")
        html = html.replace("src=\"https://", "src=\"" + host_url + "https://")
        html = html.replace("src=\"http://", "src=\"" + host_url + "http://")
        html = html.replace("src=\"//", "src=\"" + host_url + url.split(":")[0] + "://")
        html = html.replace("src=\"/", "src=\"" + host_url + "/".join(url.split("/")[:3]) + "/")
        html = html.replace("src='https://", "src='" + host_url + "https://")
        html = html.replace("src='http://", "src='" + host_url + "http://")
        html = html.replace("src='//", "src='" + host_url + url.split(":")[0] + "://")
        html = html.replace("src='/", "src='" + host_url + "/".join(url.split("/")[:3]) + "/")
        html = html.replace("hxxp", "http")
        res_data = html.encode()
    else:
        res_data = res.content
    res_headers = [(k, v) for k, v in res.headers.items()]
    status = "{} {}".format(res.status_code, res.reason)
    start_response(status, res_headers)
    return [res_data]
