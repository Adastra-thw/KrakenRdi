################# FRAMEWORK LAYER ################# 
In <REDTEAM_TOOLS>/frameworks you will find  the following tools in Frameworks:

Metasploit Framework:
The popular explotaitation Framework. In this installation there's no database connection, but you can create a new connection very easily with db_connect command. You can use the default settings of the PostgreSQL engine installed or your own if you set it.
	db_connect userdb:password@127.0.0.1/database_pg 
Remember to check if PostgreSQL is started before execute this command in msfconsole.

BeEF:
BeEF is short for The Browser Exploitation Framework. It is a penetration testing tool that focuses on the web browser.
By default in this installation there's no special configuration. Before to run the server you should change the "beef.credentials.passwd" in config.yaml. You will see this message when you try to run BeEF, so you know, let change this property :)

BetterCap:
The Swiss Army knife for 802.11, BLE and Ethernet networks reconnaissance and MITM attacks. 
