# docker-puller ![License MIT](https://go-shields.herokuapp.com/license-MIT-blue.png)

[![Travis-CI Status](https://secure.travis-ci.org/glowdigitalmedia/docker-puller.png?branch=master)](http://travis-ci.org/#!/glowdigitalmedia/docker-puller)

Listen for web hooks (i.e: from docker.io builds) and run a command after that.

## Introduction
If you use docker.io (or any similar service) to build your Docker container, it may be possible that, once the new image is generated, you want your Docker host to automatically pull it and restart the container.

Docker.io gives you the possibility to set a web hook after a successful build. Basically it does a POST on a defined URL and send some informations in JSON format.

docker-puller listen to these web hooks and can be configured to run a particular script, given a specific hook.

## Setup 
It runs on Python 3. First install the requirements with `pip install -r requirements.txt`.

Set up a configuration, that is change `config.json`. Example docker-puller configuration:

    {
        "port": 8000,
        "token": "abc123",
        "hooks": {
            "myhook1": "restart-container-myhook1.sh"
        }
    }

Now add the hook to your Docker.io-setup like this: `https://myserver.com/dockerhook?token=abc123&hook=myhook1`
    
    
## Nginx-setup
You'll need Nginx (or something similar) to pass the requests along to this script. The following Nginx-configuration will do that for you:

    server {
        listen 80;
        server_name yourdomainname;
        location /dockerhook {
            proxy_pass http://localhost:8000;
        }
    }
    
To keep it running you can use something like [Upstart](http://upstart.ubuntu.com/). A simple Upstart-configuration:

    start on runlevel [2345]
    stop on runlevel [016]

    respawn
    cd /path/to/project/docker-puller/dockerpuller
    exec python3 app.py

Save as `docker-puller.conf` and place in `/etc/init/` on your Ubuntu system.



