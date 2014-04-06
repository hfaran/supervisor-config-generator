#!/usr/bin/env python

from inspect import cleandoc
from jinja2 import Template

from query_yes_no import query_yes_no


def get_template(inet_http_server=False):
    """Returns template"""
    template = ""
    if inet_http_server:
        template += cleandoc("""
        [inet_http_server]
        port=0.0.0.0:{{ inet_port }}
        username={{ inet_username }}
        password={{ inet_password }}
        """) + "\n\n"
    template += cleandoc("""
    [unix_http_server]
    file=/tmp/{{ program_name }}-supervisor.sock

    [supervisord]
    logfile=/var/log/{{ program_name }}/{{ program_name }}-supervisord.log
    logfile_maxbytes=10MB
    logfile_backups=10
    loglevel=warn
    pidfile=/var/run/{{ program_name }}-supervisord.pid
    nodaemon=false
    minfds=1024
    minprocs=200
    user=root
    childlogdir=/var/log/{{ program_name }}/

    [rpcinterface:supervisor]
    supervisor.rpcinterface_factory = supervisor.rpcinterface:make_main_rpcinterface

    [supervisorctl]
    prompt = {{ program_name }}
    serverurl=unix:///tmp/{{ program_name }}-supervisor.sock

    {% for pid in range(num_proc) %}
    [program:{{ program_name }}-{{ pid }}]
    command={{ command }}
    stderr_logfile = /var/log/{{ program_name }}/stderr.log
    stdout_logfile = /var/log/{{ program_name }}/stdout.log
    {% endfor %}
    """)

    return Template(cleandoc(template))


if __name__ == '__main__':
    inet_http_server = query_yes_no(
        "Would you like an inet_http_server section?"
    )
    kwargs = {}
    if inet_http_server:
        kwargs["inet_port"] = raw_input(
            "Enter desired inet_http_server port: "
        )
        kwargs["inet_username"] = raw_input(
            "Enter desired inet_http_server username: "
        )
        kwargs["inet_password"] = raw_input(
            "Enter desired inet_http_server password: "
        )
    kwargs["program_name"] = raw_input("Enter name of program: ")
    kwargs["command"] = raw_input("Enter command to run to start program: ")
    kwargs["num_proc"] = int(raw_input(
        "Enter number of instances to run of program: "
    ))

    print("")
    print(get_template(inet_http_server).render(**kwargs))
