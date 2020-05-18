# Stop and Wait Protocol
The purpose of this repository is to create a stop and wait protocol bewtween multiple receivers and analyze the result.

## Creating the servers
The makefile.txt contains specific instructions about how to edit the number of containers running. By running the runContainsers.sh script, you will start the environment with three receivers and one client (this was the file created for submitting the assignment with general results). By default, you will also be dropped into the workind directory of the client so that you can issue commands to initiate file transfers.

Below is an an example command that can be used once in the client:

```bash
python3 p2mpclient.py 172.17.0.3 172.17.0.4 172.17.0.5 7735 testDoc.txt 500
```

There are three main arguments here. The first is a list of IPs that can be as the number of active receiver containers. The next is the port (will not change unless otherwise configured), followed by the file to transfer and the maximum segment size (MSS) which dictates how many bytes the program will buffer.
