import os
import errno
import sys

from twisted.python import log
from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
from twisted.application.internet import MulticastServer

import requests

_fileserver = ""
_file_list = "teiler-list.txt"

def get_file_urls(url):
    full_url = "http://" + url + "/" + _file_list
    r = requests.get(full_url)
    if r.status_code == 200:
        save(r.content, _file_list)
        utils.make_files()
    else:
        print "Fileserver not at specified address"
          
def save(stuff, name):
    with open(name, 'w') as f:
        f.write(stuff)
            
class MulticastClientUDP(DatagramProtocol):
    
    def __init__(self):
        self.host = '224.0.0.5'

    def startProtocol(self):
        # this could be placed in a config
        self.transport.joinGroup(self.host)

    def stopProtocol(self):
        pass

    def datagramReceived(self, datagram, address):
        log.msg("Received: " + repr(datagram))
        # switch to a local instance variable
        global _fileserver
        _fileserver = repr(datagram).replace("'", "")
        # kill connection 
        self.transport.loseConnection()
        reactor.stop()    

def main():
    log.msg("Starting listener")
    reactor.listenMulticast(8005, 
                            MulticastClientUDP(),
                            listenMultiple = True)
    reactor.run()
    # async **should** be over
    if _fileserver != "":
        log.msg("Fileserver located at {0}".format(_fileserver))
        get_file_urls(_fileserver)


if __name__ == '__main__':
    main()
