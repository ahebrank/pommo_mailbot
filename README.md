pommo_mailbot
=============

Cron job to restart throttled pommo MTA when it fails to respawn

We've had problems with the poMMo mailing agent failing to respawn during large, throttled jobs.  This script is a workaround intended to be run as a cron job: it logs in to the admin interface, checks the status of the mailing, and forces an MTA restart if the log hasn't been updated recently enough.

It's a hack, but works for us on a host that limits us to 500 emails/hour. We run this as a cron job every 5 minutes.

Requires the following Python packages, which our host had pre-installed:

urllib
urllib2
cookielib
json
datetime
re
