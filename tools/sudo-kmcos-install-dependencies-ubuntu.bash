#!/bin/bash -eu


echo "Simple wrapping script that resolves"
echo "dependency within the APT system"

cd ~
mkdir kmcosInstallation
cd kmcosInstallation
sudo apt-get install gfortran
sudo apt-get install git
sudo apt-get install python3
sudo apt-get install python3-pip
git clone http://www.github.com/kmcos/kmcos
cd kmcos
python3 setup.py install --user
pip3 install kmcos[MINIMAL] --upgrade --user
cd examples
python3 MyFirstModel_AB.py
kmcos export MyFirstModel_AB.ini
cd MyFirstModel_AB_local_smart
kmcos benchmark
echo "if the kmcos benchmark test worked, your installation is complete!"
cd ..
cd ..
rm sudo-kmcos-install-dependencies-ubuntu.bash