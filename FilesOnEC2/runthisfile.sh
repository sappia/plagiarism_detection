# Description: This script gets ami launch index id and instance number from metadata and saves in text
# files for other python scripts to use

curl http://169.254.169.254/latest/meta-data/ami-launch-index/ -o /home/ubuntu/index.txt

curl http://169.254.169.254/latest/dynamic/instance-identity/document/instanceId -o /home/ubuntu/instance.txt