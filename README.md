# Kraken: Rapid Deployment Infrastructure for Red Teaming and Penetration Testing (aka: KrakenRDI)

KrakenRDI is a project to easily deploy Docker containers with a full toolbox for RedTeaming and Penetration Testing. Using KrakenRDI you don't need to waste time creating and setting up the environment for you and/or your team. Using KrakenRDI there's more than 50 tools and you can choose which ones should be installed in your environment.

**KrakenRDI** is a project to helps you with the setup of your environment so you don't need to strunggle with Kali, ParrotOS or similar distributions to get working your environment, stop to waste the valueable resourses of your own system with heavy virtual machines or try to find the reason why your tools in that distributions don't works as expected. Just use containers and work alone or in team.

## Features

- Build and deployment of containers with only the tools that you need or want to use.
- Useful for penetration testing audits or RedTeaming campaings 
- Tools always updated with the latests versions from GitHub or any other kind of repositories/sources. Obviously, it depends on the tool you select.
- WebUI to easily configure your container with the tools of your choice. (TO-DO)
- Images already prepared in DockerHub, so you can use it directly in your own system if you want.
- Modular and granual building of containers. You can  create individual containers for a particular stages in a RedTeaming campaing. For example, you can create a container with the tools and some documentation for the reconnaissance, weaponization, later movements, exfiltration, or any other stage.
- You can create and destroy containers easily, without leaving traces or wasting the resources of your system like virtual machines.
- Simple Rest API to control the images building and containers construction.  

## Architecture

The base architecture is composed by a full set of images for every stage in a Red Teaming campaign following the standard methodology. Every image or layer, have a lot of tools tested and widely used in this kind of tasks.

![Architecture](https://github.com/Adastra-thw/KrakenRdi/blob/master/docs/Architecture.png)


## Installation

On Debian-based systems:
`apt update && apt-get -y install python3 python3-dev redis-server`

Also, you need to install MongoDB Community Edition: https://docs.mongodb.com/manual/installation/  

And Docker-CE depending on your system: https://docs.docker.com/engine/install/  

# Usage

After install dependencies, you can use the images directly or use the Python application:

## Docker images

You can build any of the Docker images created in KrakenRDI, using this repository and the Dockerfiles located in `<KRAKENRDI_ROOT_DIR>/core/docker` or the DockerHub images.

### Building Docker images

If you want to build an image downloaded from this repository:

Build the image only with tools for anonimity.

**`cd  <KRAKENRDI_ROOT_DIR>/core/docker`**
**`docker build -t adastra/krakenrdi:anon -f Dockerfile-anon .`**

Build the image only with tools for recon.
**`cd  <KRAKENRDI_ROOT_DIR>/core/docker`**

**`docker build -t adastra/krakenrdi:recon -f Dockerfile-recon .`**

Build the image with specified tools (all of them updated): NMAP, SpiderFoot, MaliciousMacroGenerator, Demiguise.
**`cd  <KRAKENRDI_ROOT_DIR>/core/docker`**

**`docker build -f Dockerfile-base -t adastraa/krakenrdi:base --build-arg RECON_NMAP=True --build-arg RECON_SPIDERFOOT=True --build-arg WEAPON_MALICIOUSMACROGENERATOR=True --build-arg WEAPON_DEMIGUISE=True .`**

> **NOTE:**  The file **Dockerfile-base** could be useful to create a image with the specified tools. However, if you don't specify that tools it just create a Debian image as base **without any tool.**
To see the full list of tools and the arg name see **Toolbox**

### Create containers

Just use the image created. Example:

**`docker run --name krakencontainer -it --rm adastraa/krakenrdi:base bash`**

## KrakenRDI Rest API and Platform Management

You can use the Python application to manage everything in automatized way. You need 2 components: **KrakenRDI API Server** and **KrakenRDI Backend Server** if you want to use the full features of this software.
**KrakenRDI API Server** starts the Rest API and enables the endpoints which allows to list, create and delete builds and containers. Every "build" just represents the image construction in the Docker service with the specified parameters (including tools available in the image and containers created from that image).
To start the API Server you just need to run the main script with '-r' switch.

**`python3 krakenrdi.py -r`**

**KrakenRDI Backend Server** starts a background server which receives jobs from the API Server to build a new image in the Docker service. It's only needed to create images using the endpoint **/build/crete** avaible in the **KrakenRDI Api Server**. To start the Backend Server you just need to run the main script with '-w' switch.

**`python3 krakenrdi.py -w`**

# Toolbox

## Common

Tools in this section can be applied for general purposes and can be very useful in aRT campaign or a pentest audit.

|Tool name                |Website                          |KrakenRDI name|Scope 
|----------------|-------------------------------|-----------------------------|----------------------------|
|THC Hydra|`https://github.com/vanhauser-thc/thc-hydra.git`            |THC_HYDRA            |common            |
|CeWL|`https://github.com/digininja/CeWL`            |CeWL            |common            |
|Postman|`https://dl.pstmn.io/download/latest/linux64`            |Postman            |common            |
|FuzzDB|`https://github.com/fuzzdb-project/fuzzdb.git`            |FuzzDB            |common            |
|DirBuster|`https://github.com/Adastra-thw/DirBuster-1.0`            |DirBuster            |common            |

## Frameworks

Tools in this section include sets of modules that can be used in multiple stages of any RT campaign or a pentest audit.

|Tool name                |Website                          |KrakenRDI name|Scope 
|----------------|-------------------------------|-----------------------------|----------------------------|
|Metasploit Framework|`https://github.com/rapid7/metasploit-framework`            |MetasploitFramework            |frameworks            |
|BeEF Browser Exploitation Framework|`https://github.com/beefproject/beef`            |BeEF            |frameworks            |
|Bettercap|`https://github.com/bettercap/bettercap`            |Bettercap            |frameworks            |

## Anon

Tools in this section helps to anonymize the interaction between the attacker and victim. Useful especially in RT campaigns.

|Tool name                |Website                          |KrakenRDI name|Scope 
|----------------|-------------------------------|-----------------------------|----------------------------|
|The Onion Router (from APT install)|`https://dist.torproject.org/`            |TOR - From Debian repository            |anon   |
|The Onion Router (from source code install)|`https://dist.torproject.org/`            |TOR - From source code            |anon   |
|TORSocks|`https://trac.torproject.org/projects/tor/wiki/doc/torsocks`            |TORSocks            |anon   |
|ProxyChains|`https://github.com/rofl0r/proxychains-ng`            |ProxyChains-ng            |anon   |

## Recon

Tools in this section helps in reconnaissance stage of a RT campaign or a pentest audit.

|Tool name                |Website                          |KrakenRDI name|Scope 
|----------------|-------------------------------|-----------------------------|----------------------------|
|Recon-NG|`https://github.com/lanmaster53/recon-ng`            |Recon-NG            |recon  |
|Photon|`https://github.com/s0md3v/Photon`            |Photon            |recon  |
|The Harvester|`https://github.com/laramies/theHarvester`            |theHarvester            |recon  |
|SkipTracer|`https://github.com/xillwillx/skiptracer`            |SkipTracer            |recon  |
|Metagoofil|`https://github.com/laramies/metagoofil`            |Metagoofil            |recon  |
|JustMetadata|`https://github.com/FortyNorthSecurity/Just-Metadata`            |JustMetadata            |recon  |
|SpiderFoot|`https://github.com/smicallef/spiderfoot`            |SpiderFoot            |recon  |
|Maltego CE|`https://www.maltego.com`            |Maltego            |recon  |
|Network Mapper (Nmap)|`https://github.com/nmap/nmap`            |Nmap            |recon  |

## Weaponization

Tools in this section helps in weaponization stage of a RT campaign.

|Tool name                |Website                          |KrakenRDI name|Scope 
|----------------|-------------------------------|-----------------------------|----------------------------|
|CVE2018_20250|`https://github.com/WyAtu/CVE-2018-20250`            |CVE2018_20250            |weaponization  |
|CVE2017_8759|`https://github.com/bhdresh/CVE-2017-8759`            |CVE2017_8759            |weaponization  |
|CVE2017_8570|`https://github.com/rxwx/CVE-2017-8570`            |CVE2017_8570            |weaponization  |
|CVE2017_0199|`https://github.com/bhdresh/CVE-2017-0199`            |CVE2017_0199            |weaponization  |
|DEMIGUISE|`https://github.com/nccgroup/demiguise`            |DEMIGUISE            |weaponization  |
|MALICIOUS MACRO GENERATOR|`https://github.com/Mr-Un1k0d3r/MaliciousMacroGenerator`            |MALICIOUSMACROGENERATOR            |weaponization  |
|OFFICEDDEPAYLOADS|`https://github.com/0xdeadbeefJERKY/Office-DDE-Payloads`            |OFFICEDDEPAYLOADS            |weaponization  |
|DONT KILL MY CAT|`https://github.com/Mr-Un1k0d3r/DKMC`            |DONTKILLMYCAT(DKMC)            |weaponization  |
|EMBEDINHTML|`https://github.com/Arno0x/EmbedInHTML`            |EMBEDINHTML            |weaponization  |
|MACRO PACK|`https://github.com/sevagas/macro_pack`            |MACRO_PACK            |weaponization  |

## Exploitation

Tools in this section helps in exploitation stage of a RT campaign or a pentest audit.

|Tool name                |Website                          |KrakenRDI name|Scope 
|----------------|-------------------------------|-----------------------------|----------------------------|
|Burp|`https://portswigger.net/burp`            |Burp            |exploitation  |
|ZAP|`https://github.com/zaproxy/zaproxy`            |ZAP            |exploitation  |
|CrackMapExec (CME) |`https://github.com/byt3bl33d3r/CrackMapExec`            |CrackMapExec            |exploitation  |
|Impacket|`https://github.com/SecureAuthCorp/impacket/`            |Impacket            |exploitation  |
|Powershell|`https://github.com/PowerShell/PowerShell/releases`            |Powershell            |exploitation  |

## Privilege Escalation

Tools in this section helps in privilege escalation stage of a RT campaign or a pentest audit. Some tools works for Windows and others for Linux.

|Tool name                |Website                          |KrakenRDI name|Scope 
|----------------|-------------------------------|-----------------------------|----------------------------|
|BeRoot|`https://github.com/AlessandroZ/BeRoot.git`            |BeRoot            |escalation  |
|LinEnum|`https://github.com/rebootuser/LinEnum`            |LinEnum            |escalation  |
|Linux_Exploit_Suggester|`https://github.com/InteliSecureLabs/Linux_Exploit_Suggester`            |Linux_Exploit_Suggester            |escalation  |
|linuxprivchecker|`https://github.com/sleventyeleven/linuxprivchecker`            |linuxprivchecker            |escalation  |
|linux-smart-enumeration|`https://github.com/diego-treitos/linux-smart-enumeration`            |linux-smart-enumeration            |escalation  |
|JAWS|`https://github.com/411Hall/JAWS`            |JAWS            |escalation  |
|WESNG|`https://github.com/bitsadmin/wesng`            |WESNG            |escalation  |
|Windows-Enum|`https://github.com/absolomb/WindowsEnum`            |Windows-Enum            |escalation  |

## Exfiltration

Tools in this section helps in exfiltration stage of a RT campaign. Useful to get information from the victim using covert channels.

|Tool name                |Website                          |KrakenRDI name|Scope 
|----------------|-------------------------------|-----------------------------|----------------------------|
|MISTICA|`https://github.com/IncideDigital/Mistica`            |MISTICA            |exfiltration  |

# Demo videos

Soon...

# Contact

If you find any problem let try to discover the root cause and open an issue. For any other matter you can contact contact with me at adastra@thehackerway.com