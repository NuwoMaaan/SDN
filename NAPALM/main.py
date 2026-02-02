import napalm
import json
from tabulate import tabulate


def main():

    driver = napalm.get_network_driver("ios") 
    output = []

    DSW1_settings = {
        "hostname": "192.168.100.1",
        "username": "admin",
        "password": "adminpassword",
    }

    
    with driver(**DSW1_settings, optional_args={"secret": "password"}) as device:
        output.append(device.get_facts())
        output.append(device.get_vlans())
        output.append(device.get_interfaces_ip())
        for i in output:
            print(json.dumps(i, indent=4))

        device.load_merge_candidate(filename="config.cfg")
        diffs = device.compare_config()
        if diffs:
            print("Differences found:")
            print(diffs)
            device.commit_config()        
        else:
            print("No differences found.")
        


if __name__ == "__main__":
    main()