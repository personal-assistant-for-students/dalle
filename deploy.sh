#!/bin/bash

echo "$SSH_PRIVATE_KEY" > private_key.pem
chmod 400 private_key.pem

ssh -o "StrictHostKeyChecking=no" -i private_key.pem ec2-user@$EC2_HOST << 'ENDSSH'
  cd /home/ec2-user/image-gen
  git pull
  ./run.sh
ENDSSH

rm -f private_key.pem