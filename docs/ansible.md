Deploy with Ansible
===================

1) Install `python2.7` on your server:

```
sudo apt update
sudo apt python2.7
```

2) Change `provisioning/inventory/prod` file - set your server address, SSH user, SSH port.

```
[prod]
prod ansible_host=<YOUR DOMAIN> ansible_ssh_user=<YOUR USER> ansible_ssh_port=<YOUR PORT> ansible_python_interpreter=python2.7
```

3) Run deploy command:

```
ansible-playbook provisioning/server.yml -l prod -e env=prod -i provisioning/inventory/prod
```

or

```
make deploy
```
