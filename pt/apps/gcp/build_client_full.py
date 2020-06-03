build_client_full = """spawn sudo docker run -it --volumes-from {ovpn_data} kylemanna/openvpn easyrsa build-client-full {host_name} nopass
expect -exact "Enter pass phrase for /etc/openvpn/pki/private/ca.key"
send -- "{pwd}{sep}"
expect eof"""
