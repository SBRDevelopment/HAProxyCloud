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

Script for HAProxy that updates the servers when new servers are added to an autoscaling group.

Based on the github project https://github.com/markcaudill/haproxy-autoscale

Dependencies
============

The following PyPi extensions are required.

* boto
* pyyaml
* argparse
* mako

Building
========

The project should be built as an RPM and then distributed to the RPM repositories. 

* ./build.sh

Installing
==========

* sudo yum install haproxy-cloud

# Must rename the cluster.yaml file if you want to use this config file or just add any .yaml file
# into the same directory and it will be loaded instead. 
mv /etc/haproxy-cloud/conf.d/cluster.yaml.sample /etc/haproxy-cloud/conf.d/cluster.yaml