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
mkdir /etc/yum.repos.d/bak && mv -f /etc/yum.repos.d/*.repo /etc/yum.repos.d/bak
tee /etc/yum.repos.d/CentOS_76.repo << EOF
[base]
name=CentOS-7.6
enabled=1
baseurl=http://yum.oss-cn-chengdu-scnx-d01-a.prod.cloud.scrcu-inc.com/centos/7.6/os/\$basearch/
gpgcheck=1
gpgkey=http://yum.oss-cn-chengdu-scnx-d01-a.prod.cloud.scrcu-inc.com/centos/RPM-GPG-KEY-CentOS-7
[updates]
name=CentOS-7.6
enabled=1
baseurl=http://yum.oss-cn-chengdu-scnx-d01-a.prod.cloud.scrcu-inc.com/centos/7.6/updates/\$basearch/
gpgcheck=1
gpgkey=http://yum.oss-cn-chengdu-scnx-d01-a.prod.cloud.scrcu-inc.com/centos/RPM-GPG-KEY-CentOS-7
[extras]
name=CentOS-7.6
enabled=1
baseurl=http://yum.oss-cn-chengdu-scnx-d01-a.prod.cloud.scrcu-inc.com/centos/7.6/extras/\$basearch/
gpgcheck=1
EOF
tee /etc/yum.repos.d/epel.repo << EOF
[epel]
name=Extra Packages for Enterprise Linux 7 - $basearch
enabled=1
failovermethod=priority
baseurl=http://yum.oss-cn-chengdu-scnx-d01-a.prod.cloud.scrcu-inc.com/epel/7/\$basearch
gpgcheck=0
gpgkey=http://yum.oss-cn-chengdu-scnx-d01-a.prod.cloud.scrcu-inc.com/epel/RPM-GPG-KEY-EPEL-7
EOF
cat >> /root/.ssh/authorized_keys << EOF
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDH4tsTqcFrR2TbYdeuaDufY/iBoLDYcxtzAAwlRFUat5R06Oto15G+qTphUAeHo11V61lvRZ3LUDpX66xwO1HrOqbfm7GTgBN/STebd3N0dAwNEp2vWN49gcbstwRVwUCUMK4ZTx5+vDW8jFj9bDc7BtqoxzyYw9yFx2nVMBiNC8M93QkhbqXtHKPyrWnWZ+MoXc/4BOp59Z0J09hk/Uvkk0NlEX0YfJnCb6uJiw7XLio0IeSuIBDSMoLymzdZVdT8/5xV4sQh/tgxT64X27qCNv/DOp3X91fx47JlJ3/h4iKOF23qZFl3lLHFxYFoFAmtnK1+30eeesWskFs/zkQN root@sx-EcsManager
EOF



