#! /usr/bin/bash
LOGFILE=/var/log/panel-bin.log
PANELDIR=/opt/panel
cd $PANELDIR
$PANELDIR/panel $@ >> $LOGFILE
echo " " >>$LOGFILE
