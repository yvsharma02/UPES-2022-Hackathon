import socket   
import ipinfo

def get_ip():

    DNS_IP = "2001:4860:4860::8888"
    PORT = 80

    soc = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
    soc.connect((DNS_IP, PORT))
    return soc.getsockname()[0]

# (Latitude, Longitutde)
def get_location():
    ACCESS_TOKEN = '22a3fe3b0f89b0'
    handler = ipinfo.getHandler(ACCESS_TOKEN)
    details = handler.getDetails(get_ip())
    return (details.latitude, details.longitude);
