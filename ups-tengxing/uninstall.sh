#!/bin/bash

if [ "$1" = "ovirt32" ]
then
  cp -f vdsm_org32 /usr/share/vdsm/vdsm
  echo "uninstalling ups on ovirt32"
else
  echo "Plz input the arg 'ovirt32' or 'ovirt35'"
  echo "ups uninstalled failed!"
  exit
fi

killall upsdaemon.py
rm -rf /usr/bin/upsdaemon.py

if grep -Fxq "/usr/bin/upsdaemon.py &" /etc/rc.d/rc.local
then
  sed -i '/\/usr\/bin\/upsdaemon.py &/d' /etc/rc.d/rc.local
else
  echo "upsdaemon.py has deleted in rc.local!"
fi
chmod a+x /etc/rc.d/rc.local
echo "restarting vdsmd ..."
service vdsmd restart
echo "upsdaemon uninstall success!"

