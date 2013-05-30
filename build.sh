#!/bin/bash

usage()
{
cat <<EOF
usage: $0 options

This script will build the prototype rpm

OPTIONS:
	-h	Show this message
	-r	Set the release number for this build
	-o	Root directory for the repo where the files should be copied
	-v	Verify that the build works ( will not copy files to repo )
	
EOF
}

RELEASE=`python bin/version`
REPO_ROOT=/var/www/html/repo
VERIFY=

while getopts "hr:o:v" OPTION
do
	case $OPTION in
		h)
			usage
			exit 0
			;;
		r)
			RELEASE=$OPTARG
			;;
		o)
			REPO_ROOT=$OPTARG
			;;
		v)
			VERIFY=1
			;;
	esac
done

# Clean the dist directory before building
rm -Rf dist

python setup.py bdist_rpm --release $RELEASE
python setup.py clean -a
rm -Rf *.egg-info

if [ -n "$VERIFY" ];
then
	exit 0
fi

# Copy the rpm files to the repo directories
# This code will only be run if the repo root was set as an argument
sudo cp dist/*.src.rpm "${REPO_ROOT}/packages/AML/SRPMS"
sudo cp dist/*.x86_64.rpm "${REPO_ROOT}/packages/AML/x86_64"

# Reload the repository cache
sudo createrepo -v $REPO_ROOT
