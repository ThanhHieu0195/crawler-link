# Welcome to crawler link
##### Config env
    apt-get update;apt-get install python3;
    apt-get install python3-pip;
    pip3 install -U python-dotenv
    
#### Server
    config .env
    python3 server.py
    
#### Client
    config .env
    python3 client.py
    
#### Schedule
    crontab -e
    30 2 * * * python3 /path-source/schedule-task.py # run schedular 2:30am