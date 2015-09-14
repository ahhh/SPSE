from socket import *

rawSocket = socket(AF_INET, SOCK_RAW, IPPROTO_TCP)
rawSocket.bind(('wlan0', 0))

while True:

    data = rawSocket.recv(2048)

    # http://en.wikipedia.org/wiki/IPv4#Packet_structure

    # Internet Header Length; Have to determine where the IP header ends
    ihl = ord(data[0]) & 15
    ip_payload = data[ihl*4:]

    # http://en.wikipedia.org/wiki/Transmission_Control_Protocol#TCP_segment_structure

    # Match SYN but not SYN/ACK
    if (ord(ip_payload[13]) & 18) == 2:
        src_addr = inet_ntoa(data[12:16])
        dst_addr = inet_ntoa(data[16:20])

        # Could use struct.unpack, might be clearer
        src_port = (ord(ip_payload[0]) << 8) + ord(ip_payload[1])
        dst_port = (ord(ip_payload[2]) << 8) + ord(ip_payload[3])

        src_str = (src_addr+':'+str(src_port)).ljust(22)
        dst_str = (dst_addr+':'+str(dst_port))

        print "%s=> %s" % (src_str, dst_str)
