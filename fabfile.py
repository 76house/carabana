from fabric.api import *

env.hosts = ['bozka@s7.wservices.ch']

def deploy():
   local('git push')
   run('cd ~/carabana; git pull')
   run(' ~/init/carabana restart')

def restart():
   run(' ~/init/carabana restart')

