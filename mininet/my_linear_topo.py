#!/usr/bin/python3

from mininet.topo import Topo


class MyTopo(Topo):
    """
    Define MyTopo class to create a custom topology.
    """

    def build(self, s=1, n=2):
        """
        Build the topology of s switches each connected to n hosts.
        """
        host_id = 1
        prev_sw = None

        for i in range(s):
            switch = self.addSwitch(f"s{i+1}")

            if prev_sw is not None:
                self.addLink(prev_sw, switch)

            # Create n hosts (h1..hn) and connect them to this switch
            for j in range(n):
                host = self.addHost(f"h{host_id}")

                # Create a link to connect host to the switch
                self.addLink(host, switch)
                host_id += 1

            prev_sw = switch


# Dictionary to define the name of the custom topology to be invoked by Mininet
topos = {"my_linear_topo": MyTopo}

