pommo_mailbot
=============

_Cron job to restart throttled pommo MTA when it fails to respawn_

We've had problems with the poMMo mailing agent failing to respawn during large, throttled jobs.  This script is a workaround intended to be run as a cron job: it logs in to the admin interface, checks the status of the mailing, and forces an MTA restart if the log hasn't been updated recently enough.

It's a hack, but works for us on a host that limits us to 500 emails/hour. We run this as a cron job every 5 minutes.

Requires the following Python packages, which our host had pre-installed:

* urllib
* urllib2
* cookielib
* json
* datetime
* re

To use, edit the following parameters in mailbot.py:

    base_url = 'FULL URL FOR BASE POMMO FOLDER'
    username = 'A POMMO ADMIN USERNAME'
    password = 'PASSWORD'
    threshold = 3

(where threshold is the number of minutes since the last logging activity--this is how the script assesses whether the MTA is stuck)

Test, and then add as a cron job running at short intervals (i.e., in cPanel).
