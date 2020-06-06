curl https://get.acme.sh | sh
root=~/pt-docker/docker-compose/haproxy
domain=$1

echo $root
echo $domain

~/.acme.sh/acme.sh --issue \
  -d $domain \
  -w ~/data/projects/wwwroot --force

cd ~/.acme.sh/$domain/
cat $domain.key $domain.cer ca.cer > $domain.pem
cp $domain.pem $root/docker-data/certs