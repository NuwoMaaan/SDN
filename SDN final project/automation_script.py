import requests, time, json
import os, subprocess
from requests.auth import HTTPBasicAuth

def main():
	onos, ryu = start_controllers()
	sw_id = get_switch_id()
	add_ISP_interfaces(sw_id)
	test_ISP_interfaces(sw_id)
	test_onos()
	try:
		print("ctrl + c to terminate program")
		while True: 
			time.sleep(1)
	except KeyboardInterrupt:
		print("stopping...")
		kill_controllers(ryu)
		
def start_controllers():
	# redirect console outputs from ONOS and Ryu to blackhole
	# Reason: Controllers output are verbose and I want to only see my scripts output
	FNULL = open(os.devnull, 'w')
	# Start ONOS
	onos = subprocess.Popen(
		["sudo", "/opt/onos/bin/onos-service", "start"],
		stdout=FNULL,
		stderr=subprocess.STDOUT,    
	)
	# Start RYU
	ryu = subprocess.Popen(
		["ryu-manager", "--verbose", "rest_router.py",
		 "gui_topology/gui_topology.py"],
		cwd="/home/sdn/Downloads/ryu/ryu/app/",
		stdout=FNULL, 
		stderr=subprocess.STDOUT,
	)

	return onos, ryu

def get_switch_id(): # -> list
	# curl -X GET http://localhost:8080/stats/switches
	# Wait for switch to connect to controller
	while True:
		time.sleep(10)
		try:
			print("\nGetting switch ID")
			r = requests.get("http://localhost:8080/stats/switches") 
			if r.status_code == 200:
				r = r.json()
				# convert switch id to hex format with leading zeros
				print("%016x" % r[0])
				return ("%016x" % r[0])
		except Exception as e:
			print(e)
	

def add_ISP_interfaces(sw_id):
	# curl -X POST -d '{"address":"10.1.1.2/24"}' http://localhost:8080/router/0000661063781143
	# Dynamic automation kinda stops here - How do we determine 
	# which switch is which based on id relative to network topology without user input?
	ipv4 = ["10.1.1.2/24", "10.2.2.2/24", "10.3.3.2/24"]
	#sw_id = "0000661063781143"	
	
	for i in range(len(ipv4)):
		payload = {"address": ipv4[i]} 
		url = "http://localhost:8080/router/%s" %sw_id
		r = requests.post(url, data=json.dumps(payload))
		
		if r.status_code == 200:
			print("Success:", r.text)
		else:
			print("Failed:", r.status_code, r.text)

def test_ISP_interfaces(sw_id):
	# curl http://localhost:8080/router/<switch-id>
	url = "http://localhost:8080/router/%s" %sw_id
	r = requests.get(url) 	
	if r.status_code == 200:
		print("\nrunning: curl http://localhost:8080/router/<switch-id>")
		print("\nVerifying ISP interface config: ", r.text)


def test_onos():
	# ONOS takes a bit longer to start up
	# ONOS requires basic user,password auth to access API endpoints
	retries = 3
	url = "http://localhost:8181/onos/v1/topology"
	auth = HTTPBasicAuth("onos", "rocks")
	while retries > 0:
		try:
			r = requests.get(url, auth=auth, timeout=30)
			if r.status_code == 200:
				print("ONOS API up")
				print(r.text)
				break
			else:
				print("waiting for ONOS...")
				retries -= 1
		except Exception as e:
			print(e)
		time.sleep(10)

def kill_controllers(ryu):
	# The initial start command for ONOS controller spawns a short lived process
	# that spawns the main ONOS process, therefore we would need to follow that pid 
	# further to terminate, however we can call the stop command which effectively stops the process
	subprocess.run(["sudo", "/opt/onos/bin/onos-service", "stop"])
	if ryu.poll() is None:
		ryu.terminate()
		ryu.wait()
	print("program has terminated controllers and exited")
		
if __name__ == "__main__":
	main()
	




