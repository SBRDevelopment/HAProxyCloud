============
HAProxyCloud
============

-------------------------------
HAProxy Python Management Tools
-------------------------------

:Author: http://github.com/SBRDevelopment
:Date: 2013-05-26
:Version: 0.0.1
:Manual section: 3
        
Description
===========

Script for HAProxy that updates the servers when new servers are added to auto scaling groups.

Dependencies
============

The following PyPi extensions are required.

* boto

Building
========

The project should be built as an RPM and then distributed to the RPM repositories. 

* ./build.sh

Installing
==========

* sudo yum install haproxy-cloud
