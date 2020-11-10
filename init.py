#!/usr/bin/python3
import sys
from os import path, mkdir
import shutil

# this mirror the default structur form a normal nginx installation
# /etc/nginx/nginx.conf
# /etc/nginx/nginx.d
# /var/www/ -> main docker-compose.yml
# /var/www/example.domain/ (docker-compose.yml)
# /var/www/example.domain/html
# /var/www/example.domain/ssl (private certifications)
# /etc/letsencrypt 

directories = { 
    'letsencrypt': '/etc/letsencrypt',
    'letsencrypt.log': '/var/log/letsencrypt',
    'nginx' : '/etc/nginx',
    'nginx.conf.d' : '/etc/nginx/conf.d',
    'www' : '/var/www',
    'nginx.log' : '/var/log/nginx',
    'docker-composer' : '/var/www',
}

configs = {
    '/etc/nginx/nginx.conf': 'tmpl/nginx.conf.tmpl',
    '/var/www/docker-compose.yml':'tmpl/docker-compose-master.yml',
}
templates = {
    'default' : 'tmpl/default.conf.tmpl', # website configuration
    'index.html' : 'tmpl/index.html.tmpl' # standard web page
}

def check_directories():
    changes = 0
    for d in directories:
        directory = directories[d]
        if not path.isdir(directory):
              mkdir(directory)
              print("created: " + directory)
              changes += 1
    if not changes:
        print("Directories exist.")

    return changes

def check_default_configurations():
    changes = 0
    for c in configs:
        try:
            f = open(str(c))
            f.close()
        except FileNotFoundError:
            shutil.copy2(str(configs[c]),str(c))
            print("Copy " + str(configs[c]) + " - >" + str(c))
            changes += 1
    if not changes:
        print("Default configuratins are exist.")
        
    return changes


def do_check():
    check_directories()
    check_default_configurations()

def help():
    do_check()
    pass

def init():
    check_directories()
    check_default_configurations()
    pass

def create_domain(domains = []):
    conf_dir = directories['nginx.conf.d'] 
    composer_dir = directories['docker-composer'] +  "/" + domains[0]
    log_dir= directories["nginx.log"] + "/" + domains[0]

    default_config = conf_dir + "/" + domains[0] + ".conf"
    try:
        f = open(default_config)
        f.close()
        print("Default configuration exist:" +default_config)
        return
    except FileNotFoundError as e:
        f = open(templates['default'],"r")
        data = f.read()
        f.close
        data = data.replace('__DOMAINS__', ' '.join(domains))
        data =data.replace('__DOMAIN__', domains[0])
        f = open(default_config,'w')
        f.write(data)
        f.close

    if not path.isdir(composer_dir):
        mkdir(composer_dir)
        #create a default html directory
        mkdir(composer_dir + "/html")
        shutil.copy2(templates['index.html'], composer_dir + "/html/index.html")

    if not path.isdir(log_dir):
        mkdir(log_dir)


if __name__ == "__main__":

    if len(sys.argv)<2:
        help()
        quit()

    do_check()
    l = sys.argv
    del l[0]
    create_domain(l)
