# Kraken: Rapid Deployment Infrastructure for Red Teaming and Penetration Testing (aka: KrakenRDI)
KrakenRDI is a project to easily deploy Docker containers with a full toolbox for RedTeaming and Penetration Testing. With KrakenRDI you don't need to waste time creating and setting up the environment for you and/or your team. Using KrakenRDI there's more than 100 tools and you can choose which ones should be installed or not in your environment.

# Welcome to Kraken: Rapid Deployment Infrastructure for Red Teaming and Penetration Testing (KrakenRDI)

**KrakenRDI** is a project to easily deploy Docker containers with a full toolbox for RedTeaming and Penetration Testing. With KrakenRDI you don't need to waste time creating and setting up the environment for you and/or your team. Using KrakenRDI there's more than 100 tools and you can choose which ones should be installed or not in your environment. Now you don't need to strunggle with Kali, ParrotOS or similar to get working your environment, stop to waste the valueable resourses of your own system with heavy virtual machines. Just use containers and work alone or in team.



## Features
 - Build and deployment of containers with only the tools that you need or want to use.
 - Useful for penetration testing audits or RedTeaming campaings 
 - Tools always updated with the latests versions from GitHub or any other kind of repositories/sources. Depending on the tool.
 - WebUI to easily configure your container with the tools of your choice.
 - Images already prepared in DockerHub, so you can use it directly in your own system if you want.
 - Modular and granual building of containers. You can  create individual containers for a particular stages in a RedTeaming campaing. For example, you can create a container with the tools and some documentation for the reconnaissance, weaponization, later movements, exfiltration, or any other stage. 
 - You can create and destroy containers easily, without leaving traces or wasting the resources of your system like virtual machines.
 -  

## Architecture:
The base architecture is composed by a full set of images for every stage in a Red Teaming campaign. Every image or layer, have a lot of tools tested and widely used in this kind of tasks. 
```mermaid
graph LR
A[Base image] -- Used by --> B(Anon Image)
A[Base image] -- Used by --> C(Recon Image)
A[Base image] -- Used by --> D(Weapon Image)
A[Base image] -- Used by --> E(Delivery Image)
A[Base image] -- Used by --> F(Exploit Image)
A[Base image] -- Used by --> G(C&C Image)
A[Base image] -- Used by --> H(Internal Image)
A[Base image] -- Used by --> I(Lateral Movements Image)
A[Base image] -- Used by --> J(Escalation Image)
A[Base image with needed dependencies] -- Used by --> K(Exfiltration Image)
B(Anon Image) -- INCLUDES --> B1(Tor, torsocks, proxychains, etc.)
C(Recon Image) -- INCLUDES --> C1(Recon-ng, SpiderFoot, TheHarvester, etc.)
D(Weapon Image) -- INCLUDES --> D1(Recon-ng, SpiderFoot, TheHarvester, etc.)
E(Delivery Image) -- INCLUDES --> E1(Recon-ng, SpiderFoot, TheHarvester, etc.)
F(Exploit Image) -- INCLUDES --> F1(Recon-ng, SpiderFoot, TheHarvester, etc.)
G(C&C Image) -- INCLUDES --> G1(Recon-ng, SpiderFoot, TheHarvester, etc.)
H(Internal Image) -- INCLUDES --> H1(Recon-ng, SpiderFoot, TheHarvester, etc.)
I(Lateral Movements Image) -- INCLUDES --> I1(Recon-ng, SpiderFoot, TheHarvester, etc.)
J(Escalation Image) -- INCLUDES --> J1(Recon-ng, SpiderFoot, TheHarvester, etc.)
K(Exfiltration Image) -- INCLUDES --> K1(Recon-ng, SpiderFoot, TheHarvester, etc.)
```
## Toolbox:

## Installation

## Contact
If you find any problem let try to discover the root cause and open an issue. For any other matter you can contact contact with me at adastra@thehackerway.com

# Markdown extensions

StackEdit extends the standard Markdown syntax by adding extra **Markdown extensions**, providing you with some nice features.

> **ProTip:** You can disable any **Markdown extension** in the **File properties** dialog.


## SmartyPants

SmartyPants converts ASCII punctuation characters into "smart" typographic punctuation HTML entities. For example:

|                |ASCII                          |HTML                         |
|----------------|-------------------------------|-----------------------------|
|Single backticks|`'Isn't this fun?'`            |'Isn't this fun?'            |
|Quotes          |`"Isn't this fun?"`            |"Isn't this fun?"            |
|Dashes          |`-- is en-dash, --- is em-dash`|-- is en-dash, --- is em-dash|


## KaTeX

You can render LaTeX mathematical expressions using [KaTeX](https://khan.github.io/KaTeX/):

The *Gamma function* satisfying $\Gamma(n) = (n-1)!\quad\forall n\in\mathbb N$ is via the Euler integral

$$
\Gamma(z) = \int_0^\infty t^{z-1}e^{-t}dt\,.
$$

> You can find more information about **LaTeX** mathematical expressions [here](http://meta.math.stackexchange.com/questions/5020/mathjax-basic-tutorial-and-quick-reference).


## UML diagrams

You can render UML diagrams using [Mermaid](https://mermaidjs.github.io/). For example, this will produce a sequence diagram:

```mermaid
sequenceDiagram
Alice ->> Bob: Hello Bob, how are you?
Bob-->>John: How about you John?
Bob--x Alice: I am good thanks!
Bob-x John: I am good thanks!
Note right of John: Bob thinks a long<br/>long time, so long<br/>that the text does<br/>not fit on a row.

Bob-->Alice: Checking with John...
Alice->John: Yes... John, how are you?
```

And this will produce a flow chart:

```mermaid
graph LR
A[Square Rect] -- Link text --> B((Circle))
A --> C(Round Rect)
B --> D{Rhombus}
C --> D
```