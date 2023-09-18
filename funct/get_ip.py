import urllib.request

# DEF: get IP
def get_ip():
    with urllib.request.urlopen(urllib.request.Request("https://ipv4.icanhazip.com")) as response:
        return str(response.read().decode('utf-8')).lstrip().rstrip()