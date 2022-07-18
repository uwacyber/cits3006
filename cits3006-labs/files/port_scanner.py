from socket import *
import argparse

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--target', dest='target', help='Target IP Address/Adresses')
    options = parser.parse_args()

    #Check for errors i.e if the user does not specify the target IP Address
    #Quit the program if the argument is missing
    #While quitting also display an error message
    if not options.target:
        #Code to handle if interface is not specified
        parser.error("[-] Please specify an IP Address or Addresses, use --help for more info.")
    return options
  
def main():
  if __name__ == '__main__':
     target = get_args().target
     t_IP = gethostbyname(target)
     print ('Starting scan on host: ', t_IP)

     for i in range(1, 1024):
        s = socket(AF_INET, SOCK_STREAM)

        conn = s.connect_ex((t_IP, i))
        if(conn == 0) :
           print ('Port %d: OPEN' % (i,))
        s.close()
  
main()
