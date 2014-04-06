Simple `supervisord.conf` Generator
===========================

`gen_supervisor_config.py` will generate a basic `supervisord.conf` for you that should be mostly suitable for many situations. Of course, it is a configuration file you're generating so feel free to configure it after it is generated or hack the template to get the output you want.

## Usage

* Install `Jinja2` and grab this repository:

```bash
sudo pip install Jinja2
git clone https://github.com/hfaran/supervisor-config-generator.git
cd supervisor-config-generator
```

* Just run `gen_supervisor_config.py` and fill in the prompts:

```bash
$ ./gen_supervisor_config.py
Would you like an inet_http_server section? [Y/n] Y
Enter desired inet_http_server port: 9001
Enter desired inet_http_server username: user
Enter desired inet_http_server password: pass
Enter name of program: mywebapp
Enter command to run to start program: ./my_web_app.py -p 80
Enter number of instances to run of program: 3
```

* From that you will get an output like this:

```
[inet_http_server]
port=0.0.0.0:9001
username=user
password=pass

[unix_http_server]
file=/tmp/mywebapp-supervisor.sock

[supervisord]
logfile=/var/log/mywebapp/mywebapp-supervisord.log
logfile_maxbytes=10MB
logfile_backups=10
loglevel=warn
pidfile=/var/run/mywebapp-supervisord.pid
nodaemon=false
minfds=1024
minprocs=200
user=root
childlogdir=/var/log/mywebapp/

[rpcinterface:supervisor]
supervisor.rpcinterface_factory = supervisor.rpcinterface:make_main_rpcinterface

[supervisorctl]
prompt = mywebapp
serverurl=unix:///tmp/mywebapp-supervisor.sock


[program:mywebapp-0]
command=./my_web_app.py -p 80
stderr_logfile = /var/log/mywebapp/stderr.log
stdout_logfile = /var/log/mywebapp/stdout.log

[program:mywebapp-1]
command=./my_web_app.py -p 80
stderr_logfile = /var/log/mywebapp/stderr.log
stdout_logfile = /var/log/mywebapp/stdout.log

[program:mywebapp-2]
command=./my_web_app.py -p 80
stderr_logfile = /var/log/mywebapp/stderr.log
stdout_logfile = /var/log/mywebapp/stdout.log
```
