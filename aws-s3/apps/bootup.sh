#!/bin/bash
set -e
sudo yum -y install python
sudo yum -y install python-pip
sudo pip install -U pip
sudo pip install --upgrade pip
sudo yum -y install python-devel mysql-devel
sudo pip install --upgrade MySQL-python
