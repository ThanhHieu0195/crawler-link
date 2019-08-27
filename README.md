# Welcome to crawler link
##### Config env
    apt-get update;apt-get install python3;
    apt-get install python3-pip;
    pip3 install -U python-dotenv
    pip3 install requests
    pip3 install pymongo
#### serversocket
    config .env
    python3 serversocket.py or Script/serversocket with log file
    
#### clientsocket
    config .env
    python3 clientsocket.py or Script/clientsocket -t ins -l clientsocket-log with log file
    
#### Schedule
    crontab -e
    30 2 * * * python3 /path-source/schedule-task.py # run schedular 2:30am
    
#### Command 
    - Generate fake data link: python3 command.py --run=fake-link
    
### Script
    Script/serversocket # comment changeport script
    Script/clientsocket -t ins -l clientsocket-ins-log
