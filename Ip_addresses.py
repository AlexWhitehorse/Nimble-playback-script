#!/usr/bin/python3.6
import ipaddress

class IPv4_ip():
    def __init__(self, ip):
        self.user_ip = ip
        self.network = None
        self.ipv4 = None
        self.ipRange_int = None
        
        if 6 < self.user_ip.find('/'):
            self.network = ipaddress.ip_network(self.user_ip)  
            self.ipRange_int = self.get_ip_int_range()
        else:
            self.ipv4 = ipaddress.ip_address(self.user_ip)
            self.ipRange_int = self.get_ip_int_range()


    def get_ip_int_range(self):
        range_ip = []
        if self.network:
            hosts = self.network
            for x in hosts:
                range_ip.append(int(x))
            return range_ip
            
        range_ip.append(int(self.ipv4))
        return range_ip

    def is_in_range(self, input_ip):
        int_ip = int(ipaddress.ip_address(input_ip))

        if int_ip in self.ipRange_int:
            return True
        else:
            return False

if __name__ == '__main__':
    myIP = IPv4_ip('91.202.108.137')
    print(myIP.is_in_range('91.202.108.137'))