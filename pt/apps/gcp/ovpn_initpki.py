
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