#!/bin/bash
set -e

EC2_HOST=ec2-18-206-220-10.compute-1.amazonaws.com

echo $SSH_PRIVATE_KEY > private_key.pem
chmod 700 private_key.pem

ssh -o "StrictHostKeyChecking=no" -i private_key.pem ec2-user@$EC2_HOST << 'ENDSSH'
  PID=$(lsof -t -i :8000)
  if [ ! -z "$PID" ]; then
    kill -9 $PID
  fi

  cd /home/ec2-user/image-gen
  git pull
  nohup bash run.sh &
ENDSSH


rm -f private_key.pem
