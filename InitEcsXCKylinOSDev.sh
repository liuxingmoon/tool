#!/bin/sh
useradd app
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
tee /etc/yum.repos.d/kylin.repo << EOF
###Kylin Linux Advanced Server 10 - os repo###
[ks10-adv-os]
name = Kylin Linux Advanced Server 10 - Os 
baseurl = http://14.60.64.242:/KylinOSrepo/\$basearch
gpgcheck = 0
enabled = 1

[ks10-adv-updates]
name = Kylin Linux Advanced Server 10 - Updates
baseurl = http://14.60.64.242:/KylinOSrepo/\$basearch
gpgcheck = 0
enabled = 1

[ks10-adv-addons]
name = Kylin Linux Advanced Server 10 - Addons
baseurl = http://14.60.64.242:/KylinOSrepo/\$basearch
gpgcheck = 0
enabled = 1
EOF
sed -i "s#set superusers=root#\#set superusers=root#g" /etc/grub2-efi.cfg
sed -i "s#password_pbkdf2 root grub#\#password_pbkdf2 root grub#g" /etc/grub2-efi.cfg
cat >> /root/.ssh/authorized_keys << EOF
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDfIvMB4aT1D1dxPqtZTPIu38SgVKEIrKh3qdgbLERKCKl33hMRhDBMzQw4mFLVDIlwrSkFRw8g2XWP/JsJzhi4Lr6SgPOvM5g5PSkAYgTZp5GKHLDwyv5HmPNDOYwtH2d8wZYJNElviPkxARRT54wzzHKuvCd+1KZDkDe9ZiWbpK4cCh5lrXxAr6NWvTcIjvFO/920XjbaOyIB9g/roFocbVMzlXoUEaa09mioInqcZZUpScPrpd+Bjro14AzD0kgQ7OH1LOvKYxlHnqhVTQ24bg48gGV4JViYlASMxN8svVMr/JSfE8CfZRMVUE6ciVn+OtCo6YKkyV5NHcnrmFBz root@iZg0k01kbexhal92xohsrcZ
EOF



