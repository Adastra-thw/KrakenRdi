################# ANON LAYER ################# 
In <REDTEAM_TOOLS>/exfiltration you will find  the following tools for exfiltrate information:

Mistica: 
Mística is a tool that allows to embed data into application layer protocol fields, with the goal of establishing a bi-directional channel for arbitrary communications. Currently, encapsulation into HTTP, HTTPS, DNS and ICMP protocols has been implemented, but more protocols are expected to be introduced in the near future. In the main directory of this tool you will find the subdirectory "dist" with the compiled client using "pyistaller". It will be useful to upload in the compromised machine and exfiltrate data directly, no need to install Python in that system.