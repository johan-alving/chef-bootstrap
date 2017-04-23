import subprocess
import time
import json
import time
import Queue
from threading import Thread

BOOTSTRAP_TEMPLATE = ""
CHEF_REPO = ""
KNIFE = ""

q = Queue.Queue()
result = {}

def load_bootstrap_template(json_file_path):
    with open(json_file_path) as json_file:
        return json.load(json_file)

def put_nodes_into_queue(nodes_to_bootstrap):
    for node in nodes_to_bootstrap:
        if node['protocol'] == 'ssh' or node['protocol'] == 'winrm':
            q.put(node)
        else:
            print("{}: {} is not an allowed protocol. Use 'ssh' or 'winrm'.".format(node['host'], node['protocol']))
            raise SystemExit()

def bootstrap():
    while not q.empty():
        node = q.get()
        with open(node['node_name'] + ".log", 'w') as log_file:
            if node['protocol'] == 'winrm':
                bootstrap_cmd = [KNIFE, 'bootstrap', 'windows', 'winrm', node['host'],
                                "-N", node['node_name'], "-r", "recipe[{}]".format(node['cookbook']),
                                "-x", node['user'], "-P", node['password'], "--yes"]
            elsif node['protocol'] == 'ssh':
                bootstrap_cmd = [KNIFE, 'bootstrap', node['host'], "-N", node['node_name'],
                                "-r", "recipe[{}]".format(node['cookbook']), "-x", node['user'],
                                "-P", node['password'], "--sudo", "--use-sudo-password",
                                "--bootstrap-version", "12.13.37", "--yes"]
            bootstrap_result = subprocess.call(bootstrap_cmd, stdout=log_file, stderr=log_file, cwd=CHEF_REPO)
        result[node['node_name']] = bootstrap_result
        q.task_done()

def main():
    nodes_to_bootstrap = load_bootstrap_template(BOOTSTRAP_TEMPLATE)
    put_nodes_into_queue(nodes_to_bootstrap)
    for node in nodes_to_bootstrap:
        print("Bootstrapping {}...".format(node['node_name']))

    threads = []
    for i in range(len(nodes_to_bootstrap)):
        t = Thread(target=bootstrap)
        threads.append(t)

    for thread in threads:
        thread.setDaemon(True)
        thread.start()
        time.sleep(5)

    for thread in threads:
        thread.join()

    print("\n")
    for node in nodes_to_bootstrap:
        if result[node['node_name']] == 0:
            print("{} bootstrapped successfully".format(node['node_name']))
        else:
            print("{} failed bootstrapping. See log {}.log".format(node['node_name'], node['node_name']))

if __name__ == '__main__':
    main()
