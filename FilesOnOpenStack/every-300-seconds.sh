# This script is made to run in background continuously. It runs dowork.py every 300 seconds
while true
do
        python /home/ubuntu/dowork.py
        sleep 300
done