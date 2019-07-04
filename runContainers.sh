# Builds the server image
docker build -t server .


# Runs all of the servers
# Add more receivers here and know that the servers IP will need to be added
# in the CLI arguments for the sender
# All IPs for the receivers start at 172.17.0.3

# Don't edit the sender container
docker run -itd --name sender server

# Add receivers here, be sure to also add them in the stopContainers.sh file
# Each of the lines below also contain the CLI arguments for the receivers
# server files.
docker run -itd --name receiver1 server python3 p2mpserver.py 7735 newFile.txt 0.05

docker run -itd --name receiver2 server python3 p2mpserver.py 7735 newFile.txt 0.05

docker run -itd --name receiver3 server python3 p2mpserver.py 7735 newFile.txt 0.05


# Enters the command line of the sender
# Substituting the string "sender" for another container like receiver1 will
# drop you into that containers command line
docker exec -it sender bash

# There are instructions in the makefile that will bring forward one of the
# receivers so that the packet lost output can be seen and the response file
# recovered
