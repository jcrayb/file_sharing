## Containers:

### Subnets:

##### Web-hosting: 172.10.1.0/24

### IPs:

Container|IP
---|---
Cloudflared (Home-Lab)| 172.10.1.2  
Nginx (web-server)| 172.10.1.3
Graph Server| 172.10.1.4
ME 330 | 172.10.1.5
File Sharing | 172.10.1.6

##### Notes:
Convention is to bind port 8000+address. Example:  
Container 172.10.1.**5** will expose port 800**5**.

## Local Processes:

|Process|Port|
|---|---|
|Cloudflared (Workflows)| NA
|Nginx (Workflows)|1000
|Workflows|7000  
