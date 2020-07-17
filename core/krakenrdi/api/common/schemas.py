'''
JSON Schema used to create a building. 
'''
createBuildSchema = {
    "type": "object",
    "properties": {
        "buildName": {  "type": "string",  
                        "maxLength": 20, 
                        "minLength": 2},
        "buildScope": { "type": "array", 
                        "minItems": 1, 
                        "items": {"enum": ["common", "frameworks", "anon", "recon", 
                                           "weaponization", "delivery", "exploitation", 
                                           "persistence", "commandcontrol", "internalrecon", 
                                           "movelaterally", "exfiltration"] }},
        "tools": {"type": "array", 
                  "minItems": 1,
                  "items": {"enum": ["THC_HYDRA", "CeWL", "Postman", "FuzzDB", 
                                    "DirBuster", "MetasploitFramework", "BeEF", 
                                    "Bettercap", "TOR - From Debian repository", 
                                    "TOR - From source code", "TORSocks", "ProxyChains-ng", 
                                    "Recon-NG", "Photon", "theHarvester", 
                                    "SkipTracer", "Metagoofil", "JustMetadata", "SpiderFoot", 
                                    "Maltego", "Nmap", "CVE2018_20250", "CVE2017_8759", "CVE2017_8570", 
                                    "CVE2017_0199", "DEMIGUISE", "MALICIOUSMACROGENERATOR", 
                                    "OFFICEDDEPAYLOADS", "DONTKILLMYCAT(DKMC)", 
                                    "EMBEDINHTML", "MACRO_PACK"] }},
        "containerProperties": {"type": "object", 
                                "required": ["USERNAME","PASSWORD"],
                                "properties": {
                                    "USERNAME": {"type": "string", 
                                                 "maxLength": 20},
                                    "PASSWORD": {"type": "string", 
                                                 "maxLength": 20},
                                    "EXPOSE_PORTS": {"type": "array", 
                                                     "minItems": 1,
                                                     "uniqueItems": True,
                                                     "items": {
                                                     "type": "number"}},
                                    "RUBY_VERSION": {"type": "string", 
                                                 "maxLength": 10},
                                    "RVM_DIR": {"type": "string", 
                                                 "maxLength": 40},
                                    "RVM_LOADER": {"type": "string", 
                                                 "maxLength": 40},   
                                    "POSTGRES_PASSWORD": {"type": "string", 
                                                 "maxLength": 20},
                                    "POSTGRES_DB_NAME": {"type": "string", 
                                                 "maxLength": 20},
                                    "POSTGRES_DB_USERNAME": {"type": "string", 
                                                 "maxLength": 20},
                                    "POSTGRES_DB_PASSWORD": {"type": "string", 
                                                 "maxLength": 20},


                                },
                                "additionalProperties": False},
        "startSSH": {"type": "boolean", 
                     "default": False},
        "startPostgres": {"type": "boolean", 
                          "default": False},
        "overwrite": {"type": "boolean", 
                          "default": False},
        "additionalProperties": False,
    },
    "required": ["buildName", "buildScope", "tools"]
}

deleteBuildSchema = {
    "type": "object",
    "properties": {
        "buildName": {  "type": "string",  
                        "maxLength": 20, 
                        "minLength": 2
                    }
    }
}

detailBuildSchema = {
    "type": "object",
    "properties": {
        "buildName": {  "type": "string",  
                        "maxLength": 20, 
                        "minLength": 2
                    }
    }
}

'''
JSON Schema used to create a container. 
'''
createContainerSchema = {
    "type": "object",
    "properties": {
        "buildName": {  "type": "string",  
                        "maxLength": 20, 
                        "minLength": 2},
        "containerName": {  "type": "string",  
                        "maxLength": 20, 
                        "minLength": 2},
        "autoRemove": {"type": "boolean", 
                        "default": True},
        "capAdd": {"type": "array", 
                    "minItems": 1,
                    "uniqueItems": True,
                    "items": {"enum": ["ALL", "CAP_CHOWN", "CAP_DAC_OVERRIDE", "CAP_DAC_READ_SEARCH", "CAP_FOWNER", "CAP_FSETID", "CAP_KILL", "CAP_SETGID", "CAP_SETUID", "CAP_SETPCAP", "CAP_LINUX_IMMUTABLE", "CAP_NET_BIND_SERVICE", "CAP_NET_BROADCAST", "CAP_NET_ADMIN", "CAP_NET_RAW", "CAP_IPC_LOCK", "CAP_IPC_OWNER", "CAP_SYS_MODULE", "CAP_SYS_RAWIO", "CAP_SYS_CHROOT", "CAP_SYS_PTRACE", "CAP_SYS_PACCT", "CAP_SYS_ADMIN", "CAP_SYS_BOOT", "CAP_SYS_NICE","CAP_SYS_RESOURCE", "CAP_SYS_TIME", "CAP_SYS_TTY_CONFIG", "CAP_MKNOD", "CAP_LEASE", "CAP_AUDIT_WRITE", "CAP_AUDIT_CONTROL", "CAP_SETFCAP", "CAP_MAC_OVERRIDE", "CAP_MAC_ADMIN", "CAP_SYSLOG", "CAP_WAKE_ALARM", "CAP_BLOCK_SUSPEND",   "CAP_AUDIT_READ"] },
                    "default": ["ALL"]
                    }, 
        "capDrop": {"type": "array", 
                    "minItems": 1,
                    "uniqueItems": True,
                    "items": {"enum": ["ALL", "CAP_CHOWN", "CAP_DAC_OVERRIDE", "CAP_DAC_READ_SEARCH", "CAP_FOWNER", "CAP_FSETID", "CAP_KILL", "CAP_SETGID", "CAP_SETUID", "CAP_SETPCAP", "CAP_LINUX_IMMUTABLE", "CAP_NET_BIND_SERVICE", "CAP_NET_BROADCAST", "CAP_NET_ADMIN", "CAP_NET_RAW", "CAP_IPC_LOCK", "CAP_IPC_OWNER", "CAP_SYS_MODULE", "CAP_SYS_RAWIO", "CAP_SYS_CHROOT", "CAP_SYS_PTRACE", "CAP_SYS_PACCT", "CAP_SYS_ADMIN", "CAP_SYS_BOOT", "CAP_SYS_NICE","CAP_SYS_RESOURCE", "CAP_SYS_TIME", "CAP_SYS_TTY_CONFIG", "CAP_MKNOD", "CAP_LEASE", "CAP_AUDIT_WRITE", "CAP_AUDIT_CONTROL", "CAP_SETFCAP", "CAP_MAC_OVERRIDE", "CAP_MAC_ADMIN", "CAP_SYSLOG", "CAP_WAKE_ALARM", "CAP_BLOCK_SUSPEND",   "CAP_AUDIT_READ"] },
                    "default": [""]
                    }, 
        "privileged": {"type": "boolean", "default": False },
        "hostname":  {  "type": "string",  
                        "maxLength": 20, 
                        "minLength": 2},
        "memoryLimit": {
                        "type": "string",  
                        "maxLength": 5, 
                        "minLength": 2 },
        "networkMode": {
                        "type": "string",  
                        "maxLength": 10, 
                        "minLength": 2,
                        "enum": ["host", "bridge", "none"],
                        "default": "host"
                        },
        "networkDisabled": {
                        "type": "boolean",  
                        "default": False},
        "readOnly": {
                        "type": "boolean",  
                        "default": False},
        "removeOnFinish": {
                        "type": "boolean",  
                        "default": False},
        "ports": {"type": "array",
                  "uniqueItems": True,
                  "items": { 
                        "type": "object",
                        "properties": {
                                "protocolHost": {"type": "string", "maxLength": 3, "enum": ["tcp","udp"]}, 
                                "portHost": {"type": "number"},
                                "protocolContainer": {"type": "string", "maxLength": 3, "enum": ["tcp","udp"] }, 
                                "portContainer": {"type": "number"}
                        },
                        "required": ["portHost", "portContainer"],
                        "additionalProperties": False,
                    },
                    "additionalProperties": False,
                },
        "volumes": {"type": "array",
                    "uniqueItems": True,
                    "items": {  "type": "object",
                                "properties": {
                                    "hostVolume": { "type": "string"},
                                    "containerVolume": {"type": "string"},
                                    "modeVolume": {"type": "string", "enum":["ro","rw"], "default": "rw"}
                            },
                            "required": ["hostVolume", "containerVolume"],
                            "additionalProperties": False,
                        },
                    "additionalProperties": False,                       
                    },
        "removeIfExists": {"type": "boolean", "default": True}, 
        "enableX11": {"type": "boolean", "default": True}
    },
    "required": ["buildName"],
}

deleteContainerSchema =  { "type": "object",
                        "properties": {
                            "containerName": {
                                "type": "string", "maxLength": 40, "minLength": 2
                            }
                        }
                }
getContainerSchema= { "type": "object",
                        "properties": {
                            "containerName": {
                                "type": "string", "maxLength": 40, "minLength": 2
                            }
                        }
                }
infoToolSchema= { "type": "object",
                    "properties": {
                    "toolName": {  "type": "string",  
                        "maxLength": 40, 
                        "minLength": 2},
                    },
                    "required": ["toolName"]
                }


filterToolSchema= { "type": "object",
                    "properties": {
                    "toolName": {  "type": "string",  
                        "maxLength": 40, 
                        "minLength": 2},
                    },
                    "required": ["toolName"]
                }

defaultsBuild={        
                "startSSH": False,
                "startPostgres": True,
                "overwrite": False,
                "containerProperties": {}
            }

defaultsContainer={
                "volumes": [],
                "ports": [],
                "removeOnFinish": False,
                "readOnly": False,
                "networkDisabled": False,
                "networkMode": "bridge",
                "capDrop": [],
                "capAdd": ["ALL"],
                "autoRemove": True,
                "hostname": "krakenrdi",
                "memoryLimit": "32g",
                "privileged": False, 
                "enableX11": True
}

defaultsTool={
                "toolStage": [  "common", "frameworks", "anon", "recon", 
                                "weaponization", "delivery", "exploitation", 
                                "persistence", "commandcontrol", "internalrecon", 
                                "movelaterally", "exfiltration"]
}