#!/bin/sh
useradd -u 500 app
echo App@159357 | passwd --stdin app
echo "app     ALL=(ALL)      NOPASSWD: /usr/bin/yum" >> /etc/sudoers
echo Scrcu@123 | passwd --stdin root
echo -e "n\np\n1\n\n\n\nw"|fdisk /dev/vdb
partprobe /dev/vdb
mkfs.xfs -f /dev/vdb1
mkdir /data && mount /dev/vdb1 /data && echo "/dev/vdb1 /data                       xfs    defaults        1 1" >> /etc/fstab
mount -a
chown -R app:app /data
mkdir /etc/yum.repos.d/bak && mv -f /etc/yum.repos.d/*.repo /etc/yum.repos.d/bak
tee /etc/yum.repos.d/UniontechOS.repo << EOF
[UniontechOS-1021a-AppStream]
name = UniontechOS $releasever AppStream
baseurl = http://10.36.64.202:/UOSrepo/UnionTechOS-20-AppStream-media-20210821.0/\$basearch
enabled = 1
gpgcheck = 0
skip_if_unavailable = 1

[UniontechOS-1021a-BaseOS]
name = UniontechOS $releasever BaseOS
baseurl = http://10.36.64.202:/UOSrepo/UnionTechOS-20-BaseOS-media-20210821.0/\$basearch
enabled = 1
gpgcheck = 0
skip_if_unavailable = 1

[UniontechOS-1021a-PowerTools]
name = UniontechOS $releasever PowerTools
baseurl = http://10.36.64.202:/UOSrepo/UnionTechOS-20-PowerTools-media-20210821.0/\$basearch
enabled = 1
gpgcheck = 0
skip_if_unavailable = 1
EOF
cat >> /root/.ssh/authorized_keys << EOF
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDMTMcxEUUdJ62KbnTomTLh32sGIwahH2ffl89OU1gDiGy2tRipjFrpSeYunq0nHdyUDPeJzOVayKba31AC079gLhdVOPY3ihceojHFAHiFWZLrcH7bKm97grANOoGVh+PugZBY5FsHuN8x/ziNRZZM2ocdmAaoM9/EqbkIjCxJV3b7WMFpJXp1Uo9OQJ5/wEntCipqSW3zXQpabb8m23gdW3HAyjYVL0luTtZx6tJ/6MMgnaQ030Q+4HAaw9SXFHYCAop2UB/rzVgBDhjrrgFb4gqju8Jv/jNdVCQO1tUT8US/O7ao1eTTgPcph8CVE29TOq25nZ60t/9XgkpZTHIR root@yum
EOF
yum install -y polkit polkit-libs
