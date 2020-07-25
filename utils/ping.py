#!/usr/bin/python3

import subprocess as sp
import platform
import re

class Server():
    def __init__(self, host, port=None):
        self.host = host
        self.port = port


    def ping(self, host=None):
        """Sends ping to server.

        Returns True if host (str) responds to a ping request.
        Remember that a host may not respond to a ping (ICMP) request even if the host name is valid.

        Returns:
          ip: (str) ip of host
          t: (str) time in ms
          pkt_tr: (str) packets transmitted
          pkt_re: (str) packets received

        """

        host = host or self.host

        # If windows use '-c'
        param = '-n' if platform.system().lower() == 'windows' else '-c'

        # Build command. Ex: "ping -c 1 meter.com"
        command = ['ping', '-q', param, '1', host]
        response = sp.Popen(command, stdout=sp.PIPE) # Store to PIPE to supress output
        stdout,_ = response.communicate() # Commmunicate to generate output

        if response.returncode == 0:
            output = stdout.decode('ASCII') # Decode to ascii
            ip = re.search(r"\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}", output).group(0)
            t = re.search(r"\d+(?=ms)", output).group(0)
            pkt_tx = re.search(r"\d+\s(?=packets)", output).group(0)
            pkt_re = re.search(r"\d+\s(?=received)", output).group(0)

            return ip, t, pkt_tx, pkt_re
            
        else:
            print(f'{host} is down!')


# ping_server.ping(host)