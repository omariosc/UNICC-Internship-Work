# UNICC Internship Work

Internship work for United Nations International Computing Centre
<br>
October 7th 2019 - October 18th 2019

Developed two production ready scripts to automate the verification of the configuration of the production environments on the Linux systems using Python: a package query which verifies package installations to set up basis for a fusion middleware environment; a web logic system confirmation script which verifies listening and established ports.

## Package Query
- Linux and Windows versions
- verifies package installations
- confirm which package versions are installed
- checks limits: ```nofile``` & ```nproc```
- checks system requirements
- creates sysreadiness csv files
- confirm readiness for system for installation
- to set up basis for a fusion middleware environment
- error log version
- change packages with either:
    - ```os-linux-requiredpackages.txt```
    - ```os-linux6-packages.txt```
    - ```os-linux7-packages.txt```

## Web Logic System Confirmation
- port scanner
- verifies listening ports
- verifies established ports
