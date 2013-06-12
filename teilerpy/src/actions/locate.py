import netifaces

# """
# The module is intended to be an abstraction that helps the user find the
# local ip address that will be used for broadcasting. As windows, linux/mac 
# handle their interfaces differently, we want the correct IP address found and used.
# """

def get_live_interface():
    """will return a list of possible IPv4 addresses"""
    # basically try for wifi first, then ethernet
    addresses = []
    local_network = ['127.0.0.1', '127.0.1.1', '127.1.1.1']

    # loop over the available network interfaces and try to get the LAN level IP
    for iface in netifaces.interfaces():
        test_iface = netifaces.ifaddresses(iface).get(netifaces.AF_INET) #narrow down to tcp ipv4

        if test_iface is not None:
            for i in test_iface:
                if i['addr'] not in local_network:
                    addresses.append(i['addr'])

    # return the address to broadcast out
    return addresses[0] 

                