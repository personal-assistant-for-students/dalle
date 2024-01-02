#!/bin/bash
set -e

echo "$SSH_PRIVATE_KEY" > private_key.pem
chmod 700 private_key.pem

ssh -vvv -o "StrictHostKeyChecking=no" -i private_key.pem ec2-user@$EC2_HOST << 'ENDSSH'
  cd /home/ec2-user/image-gen
  git reset --hard
  git pull
  chmod +x run.sh
  ./run.sh
ENDSSH


rm -f private_key.pem