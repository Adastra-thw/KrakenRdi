################# ANON LAYER ################# 
In <REDTEAM_TOOLS>/anon you will find  the following tools for anonymize your communications:

TOR: 
If you specify to install The Onion Router as a service in the system, you Just need to run /etc/init.d/tor <status|start|stop|restart> to manage it.
On other hand, if you choose to install the latest TOR version from source code, to start the TOR instance you need to run <ANON_DIRECTORY>/tor-latest/src/app/tor -f <ANON_DIRECTORY>/torrc
You can edit or include your own torrc file if you want. 

ProxyChains: This tool is installed in the system. Just run "proxychains <command>" after add your proxies in /etc/proxychains.conf

TorSocks: This is installed in the system. Just run ". torsocks on" to enable torsocks in wide system. You need to run Tor first to open the SOCKS proxy of the Tor Instance.

TorBrowser: If you want to run this program, need to run "xhost +" to allow the connections from the Docker container to the host system. If you don't do that you can't run any program that needs X11 GUI interfaces, including TorBrowser. 
To create the container you should run with: 
-e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix 