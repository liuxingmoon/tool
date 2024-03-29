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
baseurl=http://yum.oss-cn-chengdu-scnx-d01-a.prod.xc.scrcu-inc.com/centos/7.6/os/\$basearch/
gpgcheck=1
gpgkey=http://yum.oss-cn-chengdu-scnx-d01-a.prod.xc.scrcu-inc.com/centos/RPM-GPG-KEY-CentOS-7
[updates]
name=CentOS-7.6
enabled=1
baseurl=http://yum.oss-cn-chengdu-scnx-d01-a.prod.xc.scrcu-inc.com/centos/7.6/updates/\$basearch/
gpgcheck=1
gpgkey=http://yum.oss-cn-chengdu-scnx-d01-a.prod.xc.scrcu-inc.com/centos/RPM-GPG-KEY-CentOS-7
[extras]
name=CentOS-7.6
enabled=1
baseurl=http://yum.oss-cn-chengdu-scnx-d01-a.prod.xc.scrcu-inc.com/centos/7.6/extras/\$basearch/
gpgcheck=1
EOF
tee /etc/yum.repos.d/epel.repo << EOF
[epel]
name=Extra Packages for Enterprise Linux 7 - $basearch
enabled=1
failovermethod=priority
baseurl=http://yum.oss-cn-chengdu-scnx-d01-a.prod.xc.scrcu-inc.com/epel/7/\$basearch
gpgcheck=0
gpgkey=http://yum.oss-cn-chengdu-scnx-d01-a.prod.xc.scrcu-inc.com/epel/RPM-GPG-KEY-EPEL-7
EOF
cat >> /root/.ssh/authorized_keys << EOF
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDMTMcxEUUdJ62KbnTomTLh32sGIwahH2ffl89OU1gDiGy2tRipjFrpSeYunq0nHdyUDPeJzOVayKba31AC079gLhdVOPY3ihceojHFAHiFWZLrcH7bKm97grANOoGVh+PugZBY5FsHuN8x/ziNRZZM2ocdmAaoM9/EqbkIjCxJV3b7WMFpJXp1Uo9OQJ5/wEntCipqSW3zXQpabb8m23gdW3HAyjYVL0luTtZx6tJ/6MMgnaQ030Q+4HAaw9SXFHYCAop2UB/rzVgBDhjrrgFb4gqju8Jv/jNdVCQO1tUT8US/O7ao1eTTgPcph8CVE29TOq25nZ60t/9XgkpZTHIR root@yum
EOF



