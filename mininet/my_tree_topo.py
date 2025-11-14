#!/usr/bin/python3

from mininet.topo import Topo

class MyTreeTopo(Topo):

    def build(self, depth=1, fanout=2):
        self.host_id = 1
        self.switch_id = 1
        # Add root switch
        root_switch = self.addSwitch(f"s{self.switch_id}")
        self.switch_id += 1
        self.create_tree(root_switch, depth, fanout)

    def create_tree(self, switch, depth, fanout):
	# Base case, check if last layer (add hosts)
        if depth == 1:
            for i in range(fanout):
                host = self.addHost(f"h{self.host_id}")
                self.host_id += 1
                self.addLink(switch, host)
            return
        # ELSE create another layer
        for i in range(fanout):
            child_switch = self.addSwitch(f"s{self.switch_id}")
            self.switch_id += 1
            self.addLink(switch, child_switch)
	    # Recursive function call
            self.create_tree(child_switch, depth - 1, fanout)

# Register topology
topos = {"my_tree_topo": MyTreeTopo}

