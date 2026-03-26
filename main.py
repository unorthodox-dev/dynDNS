#!/usr/bin/env python3
import os
import sys
import boto3
import requests

DOMAIN = os.environ["DDNS_DOMAIN"]
ZONE_NAME = os.environ["DDNS_ZONE_NAME"]
TTL = int(os.environ.get("DDNS_TTL", "300"))

def get_public_ip():
    try:
        resp = requests.get("https://api.ipify.org", timeout=10)
        resp.raise_for_status()
        return resp.text.strip()
    except Exception as e:
        print(f"Failed to get public IP: {e}", file=sys.stderr)
        sys.exit(1)

def get_hosted_zone_id(client, zone_name):
    zones = client.list_hosted_zones_by_name(DNSName=zone_name.rstrip("."))
    for zone in zones["HostedZones"]:
        if zone["Name"].rstrip(".") == zone_name.rstrip("."):
            return zone["Id"].split("/")[-1]
    raise RuntimeError(f"Hosted zone for {zone_name} not found")

def get_current_dns_ip(client, zone_id, fqdn):
    records = client.list_resource_record_sets(
        HostedZoneId=zone_id,
        StartRecordName=fqdn,
        StartRecordType="A",
        MaxItems="1",
    )["ResourceRecordSets"]

    if records and records[0]["Name"].rstrip(".") == fqdn.rstrip("."):
        values = records[0].get("ResourceRecords", [])
        if values:
            return values[0]["Value"]
    return None

def update_dns_record(client, zone_id, fqdn, ip):
    print(f"Updating {fqdn} -> {ip}")
    client.change_resource_record_sets(
        HostedZoneId=zone_id,
        ChangeBatch={
            "Comment": "DDNS update",
            "Changes": [
                {
                    "Action": "UPSERT",
                    "ResourceRecordSet": {
                        "Name": fqdn,
                        "Type": "A",
                        "TTL": TTL,
                        "ResourceRecords": [{"Value": ip}],
                    },
                }
            ],
        },
    )

def main():
    ip = get_public_ip()
    client = boto3.client("route53")
    zone_id = get_hosted_zone_id(client, ZONE_NAME)
    current_ip = get_current_dns_ip(client, zone_id, DOMAIN)

    if current_ip != ip:
        update_dns_record(client, zone_id, DOMAIN, ip)
        print("DNS updated.")
    else:
        print("No change detected; DNS is up to date.")

if __name__ == "__main__":
    main()
