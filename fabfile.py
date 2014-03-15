import os

from fabric.api import env, task, run, sudo, cd


keyfile = os.path.expanduser('~/.ssh/hackathon.pem')

if not os.path.isfile(keyfile):
    raise Exception('Please put hackathon.pem in ~/.ssh/')


env.host_string = 'ubuntu@hack.joel.io'
env.key_filename = keyfile


@task
def uptime():
    run('uptime')


@task
def deploy():
    with cd('/home/ubuntu/hackathon'):
        run("find . -name '*.pyc' -exec rm {} \;")
        run('git fetch -p')
        run('git rebase origin/master')
        sudo('cp deployment/hackathon.conf /etc/init/hackathon.conf')
        run('virtualenv/bin/pip install -r requirements/base.txt')
        #run("npm install")
        #run("grunt")
    restart()


@task
def restart():
    sudo('service hackathon restart')
    sudo('service nginx restart')
