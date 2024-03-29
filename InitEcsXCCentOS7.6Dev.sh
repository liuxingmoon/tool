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
baseurl=http://yum.oss-cn-chengdu-scnx-d01-a.dev.xc.scrcu-inc.com/centos/7.6/os/\$basearch/
gpgcheck=1
gpgkey=http://yum.oss-cn-chengdu-scnx-d01-a.dev.xc.scrcu-inc.com/centos/RPM-GPG-KEY-CentOS-7
[updates]
name=CentOS-7.6
enabled=1
baseurl=http://yum.oss-cn-chengdu-scnx-d01-a.dev.xc.scrcu-inc.com/centos/7.6/updates/\$basearch/
gpgcheck=1
gpgkey=http://yum.oss-cn-chengdu-scnx-d01-a.dev.xc.scrcu-inc.com/centos/RPM-GPG-KEY-CentOS-7
[extras]
name=CentOS-7.6
enabled=1
baseurl=http://yum.oss-cn-chengdu-scnx-d01-a.dev.xc.scrcu-inc.com/centos/7.6/extras/\$basearch/
gpgcheck=1
EOF
tee /etc/yum.repos.d/epel.repo << EOF
[epel]
name=Extra Packages for Enterprise Linux 7 - $basearch
enabled=1
failovermethod=priority
baseurl=http://yum.oss-cn-chengdu-scnx-d01-a.dev.xc.scrcu-inc.com/epel/7/\$basearch
gpgcheck=0
gpgkey=http://yum.oss-cn-chengdu-scnx-d01-a.dev.xc.scrcu-inc.com/epel/RPM-GPG-KEY-EPEL-7
EOF
cat >> /root/.ssh/authorized_keys << EOF
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDfIvMB4aT1D1dxPqtZTPIu38SgVKEIrKh3qdgbLERKCKl33hMRhDBMzQw4mFLVDIlwrSkFRw8g2XWP/JsJzhi4Lr6SgPOvM5g5PSkAYgTZp5GKHLDwyv5HmPNDOYwtH2d8wZYJNElviPkxARRT54wzzHKuvCd+1KZDkDe9ZiWbpK4cCh5lrXxAr6NWvTcIjvFO/920XjbaOyIB9g/roFocbVMzlXoUEaa09mioInqcZZUpScPrpd+Bjro14AzD0kgQ7OH1LOvKYxlHnqhVTQ24bg48gGV4JViYlASMxN8svVMr/JSfE8CfZRMVUE6ciVn+OtCo6YKkyV5NHcnrmFBz root@iZg0k01kbexhal92xohsrcZ
EOF




