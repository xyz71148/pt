#!/bin/sh

## generate files
generate_folder()
{
	if [ ! -d $1 ];
	then
		mkdir -p $1
	fi
}

generate_folder /app/tools/sshd;
generate_folder /var/run/sshd;

## generate host key
generate_host_key()
{
	if [ ! -f /etc/ssh/$1 ];
	then
		ssh-keygen -q -N '' -t rsa -f /etc/ssh/$1
	fi
}

generate_host_key ssh_host_ecdsa_key;
generate_host_key ssh_host_ed25519_key;
generate_host_key ssh_host_rsa_key;
generate_host_key ssh_host_dsa_key;

## process sshd config
sed -ri 's/#PermitRootLogin\s+yes/PermitRootLogin yes/g' /etc/ssh/sshd_config
sed -i "s/.*PasswordAuthentication.*/PasswordAuthentication no/g" /etc/ssh/sshd_config
sed -i "s/#MaxStartups.*/MaxStartups 10000/g" /etc/ssh/sshd_config
sed -i "s/#PermitUserEnvironment.*/PermitUserEnvironment yes/g" /etc/ssh/sshd_config

mkdir -p /root/.ssh
echo "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCuNLCUI6AP+og2FsR7bJSHVWPt8F3FnJbetFSIuCoSi92jgdO8TTfmTgiFfDyLmEVf1GF/5E73a3DMkDNaZR5iOPLODdTSmzK2uVG5e1h+cyZ1rxX7/yM2Jq+na2GajmMZ2o/nPtV6Oti5c9HcIl8pU+jarXSF8/KI9nBCJ/Lpo0wdWYj7XejMuVIVD8W2x5xPXE6G3kym6hYFg3EJVG6cKpjSw9ftr2A81LWeuV5MsbL0jjh9mXxEV3VtK3/CQgpIxsKHM2f6nmdIlqwK9p68VrclFEjZ5o2j/JNfO7fNnxXN/F3N382avKIucOXZkWjkHIlsrxa9bnSL+fByqyZF xyz@01" > /root/.ssh/authorized_keys

chmod g-w /root
chmod 700 /root/.ssh
chmod 600 /root/.ssh/authorized_keys
