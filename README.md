cmk_wrapper
===========

Problem: CheckMK is being checked in a given time interval (default 60 seconds). If you have plugins which do not need this short interval and should be run with their own interval, you need this wrapper. 

Since Version 1.2.3.i1 of CheckMK this is built in, but prior you need this!
See:  http://lists.mathias-kettner.de/pipermail/checkmk-de/2014-January/003930.html

Installation:

 Download the cmk_wrapper.py to some location.

 In /etc/check_mk/mrpe.cfg insert your plugin (-p) with the wrapper and give the interval (-i) in seconds:

 ```
 YourCheck		/usr/local/nagios-plugins/cmk_wrapper.py -i 7200 -p /usr/local/nagios-plugins/your_original_check
 ```


