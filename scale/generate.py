#!/usr/bin/env python

import os, sys, time
import jinja2, paramiko

def generateDirectories(owd):

    tiers = ["database-tier", "app-tier", "web-tier"]

    for tier in tiers:
    	if not os.path.exists(owd + "/rendered/" + tier):
        	os.makedirs(owd + "/rendered/" + tier)


def generateTemplates(owd, templatePath, count):

    os.chdir(templatePath)

    loader = jinja2.FileSystemLoader(templatePath)
    jenv = jinja2.Environment(loader=loader, trim_blocks=True, lstrip_blocks=True)
    template = jenv.get_template("database-tier.j2")

    os.chdir(owd)

    for i in range(1, int(count) + 1):
    	hello = template.render(counter=i)
        file = open("rendered/database-tier/database-tier-" + str(i) + ".yaml", "w")
	file.write(hello)
	file.close()

	print "Successfully created database-tier-" + str(i) + ".yaml"

def main():

    templatePath = os.getcwd() + "/templates/"
    count = sys.argv[1]
    owd = os.getcwd()

    generateDirectories(owd)
    generateTemplates(owd, templatePath, count)

if __name__ == '__main__':
    sys.exit(main())
