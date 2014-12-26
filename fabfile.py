#-*- coding:utf-8 -*-

import os
from fabric.api import settings, abort, put, cd, env, local, prefix
from fabric.contrib.files import exists, append
from cuisine import run, sudo


env.hosts = ['127.0.0.1:2222']
env.user = 'vagrant'
env.key_filename = [os.path.expanduser('~/.vagrant.d/insecure_private_key')]

venv_snippet = """
if [ -f /usr/bin/virtualenvwrapper.sh ]; then
    export WORKON_HOME=$HOME/.virtualenvs
    source /usr/bin/virtualenvwrapper.sh
fi
"""


def bootstrap():
    install_nginx()
    install_python27()
    install_requirements()
    start_uwsgi()
    start_nginx()


def install_nginx():
    sudo('yum -y install nginx')
    if exists('/vagrant/skelton.conf') and not exists('/etc/nginx/conf.d/skelton.conf'):
        sudo('ln -s /vagrant/skelton.conf /etc/nginx/conf.d/skelton.conf')


def install_python27():
    sudo('yum -y groupinstall "Development tools"')
    sudo('yum -y install zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel')
    sudo('yum -y install python-virtualenvwrapper')
    append('~/.bashrc', venv_snippet)

    if exists('/opt/python27'):
        return
    sudo('mkdir /opt/python27')
    with cd('/tmp'):
        run('curl -O https://www.python.org/ftp/python/2.7.6/Python-2.7.6.tgz')
        run('tar zxf Python-2.7.6.tgz')
        with cd('Python-2.7.6'):
            run('./configure  --prefix=/opt/python27')
            run('make')
            sudo('make install')
        run('rm -rf Python-2.7.6*')


def install_requirements():
    with cd('/vagrant'):
        if not exists('./requirements.txt'):
            return
        res = run('workon python27', quiet=True)
        if res.failed:
            run('mkvirtualenv python27 --python=/opt/python27/bin/python2.7')
        with prefix('workon python27'):
            run('pip install -r ./requirements.txt')


def start_uwsgi():
    with cd('/vagrant'), prefix('workon python27'):
        run('uwsgi --ini uwsgi.ini &')


def start_nginx():
    sudo('/etc/init.d/nginx start')

def restart_nginx():
    sudo('/etc/init.d/nginx restart')
