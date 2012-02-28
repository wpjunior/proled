#!/bin/sh
#
# SAPL restart script
#
echo 'Restarting SAPL server...'
/var/interlegis/SAPL-2.3/instances/sapl23/bin/zopectl restart
