#!/bin/sh
#
# SAPL shutdown script
#
echo 'Stopping SAPL server...'
/var/interlegis/SAPL-2.3/instances/sapl23/bin/zopectl stop
