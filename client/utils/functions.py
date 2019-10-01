import socket

def get_ip_adress():
    ip_address = '';
    connected = False
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while not connected:
        connected = True
        try:
            s.connect(("8.8.8.8", 80))
        except:
            connected = False

    ip_address = s.getsockname()[0]
    s.close()
    return ip_address