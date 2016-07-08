#!/usr/bin/env python
"""
    Script to configure Interface
"""
import os, sys, time
import jinja2, paramiko


def ifaceConf(iface_name, iface_desc, iface_ipv4_add, iface_ipv4_mask, templatePath):

    os.chdir(templatePath)
    loader = jinja2.FileSystemLoader(os.getcwd())
    jenv = jinja2.Environment(loader=loader, trim_blocks=True, lstrip_blocks=True)

    template = jenv.get_template("iface.j2")
    push = str(template.render(iface_name=iface_name, iface_desc=iface_desc, iface_ipv4_add=iface_ipv4_add, iface_ipv4_mask=iface_ipv4_mask)).split("\n")

    return push

def main():

    templatePath = "/home/netman/jinjaTemplating/templates"

    ip = sys.argv[1]
    iface_name = sys.argv[2]
    iface_desc = sys.argv[3]
    iface_ipv4_add = sys.argv[4]
    iface_ipv4_mask = sys.argv[5]

    remote_conn_pre=paramiko.SSHClient()
    remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    remote_conn_pre.connect(ip, port=22, username="cisco", password="cisco", look_for_keys=False, allow_agent=False)
    remote_conn = remote_conn_pre.invoke_shell()
    remote_conn.send("terminal length 0\n")
    remote_conn.send("conf t\n")
    #remote_conn.send("interface fa1/0" + "\n")
    #remote_conn.send("shut\n")
    time.sleep(1)

    pushList = ifaceConf(iface_name, iface_desc, iface_ipv4_add, iface_ipv4_mask, templatePath)

    #print pushList

    for command in pushList:
        cmd = command + "\n"
        #print cmd
        remote_conn.send(cmd)

if __name__ == '__main__':
    sys.exit(main())
