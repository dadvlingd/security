#!/bin/bash

if [ "$1" = "ovirt32" ]
then
  cp -f vdsm32 /usr/share/vdsm/vdsm
  echo "installing ups on ovirt32"
else
  echo "Plz input the arg 'ovirt32' or 'ovirt35'"
  echo "ups installed failed!"
  exit
fi

vmPath="/home/vm_params"
if [ ! -x "$vmPath" ]; then
  mkdir "$vmPath"
  chown -R 36:36 "$vmPath"
fi

cp -f upsdaemon.py /usr/bin/
if grep -Fxq "sleep 3" /etc/rc.d/rc.local
then
  echo "have sleep 3"
else
  sed -i '$a\sleep 3' /etc/rc.d/rc.local
fi

if grep -Fxq "/usr/bin/upsdaemon.py &" /etc/rc.d/rc.local
then
  echo "upsdaemon.py has added in rc.local!"
else
  sed -i '$a\/usr/bin/upsdaemon.py &' /etc/rc.d/rc.local
fi
chmod a+x /etc/rc.d/rc.local
echo "restarting vdsmd ..."
service vdsmd restart
echo "upsdaemon install success!"
chk=`ps -ef | grep 'upsdaemon.py' | grep -v grep | wc -l`
if [ $chk -eq 0 ]
then
  upsdaemon.py &
else
  killall upsdaemon.py
  upsdaemon.py &
fi
echo "start upsdaemon.py success"
