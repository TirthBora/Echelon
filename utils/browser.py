import webbrowser

def open_browser(port):
    url = f"http://127.0.0.1:{port}"
    print(f"Opening {url}")
    webbrowser.open(url)