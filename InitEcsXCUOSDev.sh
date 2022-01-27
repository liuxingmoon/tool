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
name = UniontechOS  AppStream
baseurl = http://14.60.64.242:/UOSrepo/UnionTechOS-20-AppStream-media-20210821.0/\$basearch
enabled = 1
gpgcheck = 0
skip_if_unavailable = 1

[UniontechOS-1021a-BaseOS]
name = UniontechOS  BaseOS
baseurl = http://14.60.64.242:/UOSrepo/UnionTechOS-20-BaseOS-media-20210821.0/\$basearch
enabled = 1
gpgcheck = 0
skip_if_unavailable = 1

[UniontechOS-1021a-PowerTools]
name = UniontechOS  PowerTools
baseurl = http://14.60.64.242:/UOSrepo/UnionTechOS-20-PowerTools-media-20210821.0/\$basearch
enabled = 1
gpgcheck = 0
skip_if_unavailable = 1
EOF
cat >> /root/.ssh/authorized_keys << EOF
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDfIvMB4aT1D1dxPqtZTPIu38SgVKEIrKh3qdgbLERKCKl33hMRhDBMzQw4mFLVDIlwrSkFRw8g2XWP/JsJzhi4Lr6SgPOvM5g5PSkAYgTZp5GKHLDwyv5HmPNDOYwtH2d8wZYJNElviPkxARRT54wzzHKuvCd+1KZDkDe9ZiWbpK4cCh5lrXxAr6NWvTcIjvFO/920XjbaOyIB9g/roFocbVMzlXoUEaa09mioInqcZZUpScPrpd+Bjro14AzD0kgQ7OH1LOvKYxlHnqhVTQ24bg48gGV4JViYlASMxN8svVMr/JSfE8CfZRMVUE6ciVn+OtCo6YKkyV5NHcnrmFBz root@iZg0k01kbexhal92xohsrcZ
EOF



