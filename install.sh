
python setup.py bdist_rpm

alien dist/haproxy-cloud-*.x86_64.rpm
dpkg -i haproxy-cloud_*_amd64.deb

python setup.py clean -a
rm -Rf dist *.egg-info *.deb