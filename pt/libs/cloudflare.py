import requests
import simplejson
import logging


class CloudFlare:
    """
    def update_ip_domain(ip, domain):
        auth_email = ""
        auth_key = ""
        obj = CloudFlare(auth_email, auth_key)
        obj.get_zone_id(domain)
        return obj.update_domain_ip(ip, domain)
    """
    headers = {
        "Content-Type": "application/json"
    }
    base_url = "https://api.cloudflare.com/client/v4"
    zone_id = None
    zone = None

    @classmethod
    def get_domain_dns_record(cls, ip, domain):
        return simplejson.dumps(
            dict(
                type="A",
                name=domain,
                content=ip,
                ttl=1,
                proxied=False
            )
        )

    @classmethod
    def split_domain(cls, domain):
        t = domain.split(".")
        zone = ".".join(t[-2:])
        record_name = domain[0:len(domain) - len(zone) - 1]
        return record_name, zone

    def __init__(self, auth_email, auth_key):
        self.headers["X-Auth-Email"] = auth_email
        self.headers["X-Auth-Key"] = auth_key

    def get_zone_id(self, domain):
        _, zone = self.split_domain(domain)
        res = requests.get(
            "{}/zones?name={}&status=active".format(self.base_url, zone),
            headers=self.headers
        )

        json = res.json()
        self.zone_id = json['result'][0]["id"]
        self.zone = zone
        return self

    def update_domain_ip(self, ip, domain):
        record_name, _ = self.split_domain(domain)
        domain = "{}.{}".format(record_name, self.zone)
        logging.info("getting dnsrecordid,ip: %s,domain: %s", ip, domain)
        res = requests.get(
            "{}/zones/{}/dns_records?type=A&name={}".format(self.base_url, self.zone_id, domain),
            headers=self.headers
        )
        json = res.json()
        logging.info("get dnsrecordid,result: %s", res.text)
        if len(json['result']) > 0:
            dnsrecordid = json['result'][0]['id']
            res = requests.put("{0}/zones/{1}/dns_records/{2}".format(self.base_url, self.zone_id, dnsrecordid),
                               data=self.get_domain_dns_record(ip, domain),
                               headers=self.headers)
            logging.info("update dnsrecordid: %s,result: %s", dnsrecordid, res.text)
        else:
            dnsrecordid = ""
            res = requests.post("{0}/zones/{1}/dns_records/{2}".format(self.base_url, self.zone_id, dnsrecordid),
                                data=self.get_domain_dns_record(ip, domain),
                                headers=self.headers)
            logging.info("add dnsrecordid,result: %s", res.text)
        return res.json()

