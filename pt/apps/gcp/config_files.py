shadowsocks_supervisor_config = """[program:shadowsocks]
command=/bin/bash -c "/usr/local/bin/ssserver -vv -c /etc/supervisor/conf_d/config.json"
directory=/root/
autostart=true
autorestart=true
priority=10
stdout_logfile=/dev/fd/1
stdout_logfile_maxbytes=0
stderr_logfile=/dev/fd/2
stderr_logfile_maxbytes=0"""

ovpn_initpki = """#exp_internal 1 # Uncomment for debug
set timeout -1
spawn sudo docker run -it --volumes-from {ovpn_data} kylemanna/openvpn ovpn_initpki
#expect -exact "Confirm removal:"
#send -- "yes{sep}"
expect -exact "Enter New CA Key Passphrase:"
send -- "{pwd}{sep}"
expect -exact "Re-Enter New CA Key Passphrase:"
send -- "{pwd}{sep}"
expect -exact "Common Name (eg: your user, host, or server name) \[Easy-RSA CA\]:"
send -- "{host_ip}{sep}"
expect -exact "Enter pass phrase for /etc/openvpn/pki/private/ca.key:"
send -- "{pwd}{sep}"
expect -exact "Enter pass phrase for /etc/openvpn/pki/private/ca.key:"
send -- "{pwd}{sep}"
expect eof"""

build_client_full = """spawn sudo docker run -it --volumes-from {ovpn_data} kylemanna/openvpn easyrsa build-client-full {host_name} nopass
expect -exact "Enter pass phrase for /etc/openvpn/pki/private/ca.key"
send -- "{pwd}{sep}"
expect eof"""

