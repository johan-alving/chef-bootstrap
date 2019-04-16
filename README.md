# Bootstrap one or more Chef nodes
This Python script will bootstrap one or more Chef nodes defined in a template. If multiple nodes are defined, they will be bootstrapped in parallel. Each bootstrap process prints output to a log file. After the script is finished, it will report successful and failed bootstraps. Log files are placed in the current working directory.

There are 3 constants that needs to be defined in the script:

- `BOOTSTRAP_TEMPLATE` - Path to the JSON bootstrap template
- `CHEF_REPO` - Path to your local Chef repo where the ".chef" folder is located
- `KNIFE` - Path to the "knife" executable

The bootstrap template is a JSON with the following format:

```
[
    {
        "host": "", 
        "node_name": "", 
        "user": "", 
        "password": "",
        "cookbook": "",
        "protocol": ""
    }
]
```
- `host` - IP or FQDN
- `node_name` - node name
- `user` - node username
- `password` - node user password
- `cookbook` - cookbook used
- `protocol` - protocol used to bootstrap. On Linux and Mac, use `ssh`. On Windows `winrm`.

Example:

```
[
    {
        "host": "172.23.58.100", 
        "node_name": "node01", 
        "user": "user", 
        "password": "1234",
        "cookbook": "nginx",
        "protocol": "ssh"
    },
    {
        "host": "172.23.58.101", 
        "node_name": "node02", 
        "user": "user", 
        "password": "1234",
        "cookbook": "nginx",
        "protocol": "ssh"
    }
]
```
