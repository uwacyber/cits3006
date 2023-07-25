import scapy.all as scapy
from scapy.layers import http
import argparse

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--interface', dest = 'interface', help = 'Interface Name for which packet is supposed to be captured.')
    options = parser.parse_args()
    
    if not options.interface:
        parser.error('[-] Please specify the name of the interface, use --help for more info.')
        
    return options.interface
  
def sniffer(interface):
    scapy.sniff(iface = interface, store = False, prn = process_packet)
    
def process_packet(packet):
    if packet.haslayer(http.HTTPRequest):
        url = get_url(packet)
        print('[+] HTTP Requests/URL Requested -> {}'.format(url), '\n')
        cred = get_credentials(packet)
        if cred:
            print('\n\n[+] Possible Credential Information -> {}'.format(cred), '\n\n')

def get_url(packet):
    return (packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path).decode('utf-8')

keywords = ('username', 'uname', 'user', 'login', 'password', 'pass', 'signin', 'signup', 'name')

def get_credentials(packet):
    if packet.haslayer(scapy.Raw):
        try:
            field_load = packet[scapy.Raw].load.decode('utf-8')
            for keyword in keywords:
                if keyword in field_load:
                    return field_load
        except:
            #had an HTTPS request that couldn't be decoded usint utf-8 so skip it
            pass
              
interface = get_args()
sniffer(interface)
