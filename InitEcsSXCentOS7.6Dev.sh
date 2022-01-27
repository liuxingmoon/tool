#!/bin/sh
useradd -u 500 app
echo Scrcu@123 | passwd --stdin root
echo App@159357 | passwd --stdin app
echo "app     ALL=(ALL)      NOPASSWD: /usr/bin/yum" >> /etc/sudoers
echo -e "n\np\n1\n\n\n\nw"|fdisk /dev/vdb
partprobe /dev/vdb
mkfs.xfs -f /dev/vdb1
mkdir /data && mount /dev/vdb1 /data && echo "/dev/vdb1 /data                       xfs    defaults        1 1" >> /etc/fstab
mount -a
chown -R app:app /data
cat >> /root/.ssh/authorized_keys << EOF
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDV0P2CFavu9Kd0ZWzHxzyAAKvBzDxx5j6yj7L0+O0LrTWvAeBzIdZZmHCsvcAm2dhi7R3n2QLfW8AGaN/slYPo8JEwyZM0YwN109rzqE9vA7iekxxwT/dGdbAY/ktKlAb8P7HbXEef5Kh5axlQ6vuGr4ElA6WmM6w2EGKR34j5m2hZ7+PV212S3fzTfA7grZmzWa7kZ5mlr8I8doYvR43svy7QYQeMTJO9kUqH55poZlK/kdJzQLuw7rOlhtkHpOsQers+Hv2ddSkqxOW3pfJOY5DsnXg/Qcf7G2XIIP1zRVq9fCECWcUxH7D8238pyINqim6WAwmgz2fwrFInqnJ1 root@iZi0e01nzciebf7iphaurlZ
EOF







