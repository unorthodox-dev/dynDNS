#!/usr/bin/env python3
import boto3
import requests
import json
import sys

DOMAIN = "home.unorthodoxdev.net"
ZONE_NAME = "unorthodoxdev.net"
TTL = 300  # seconds

def get_public_ip():
    try:
        return requests.get("https://api.ipify.org").text.strip()
    except Exception as e:
        print("Failed to get public IP:", e)
        sys.exit(1)

def get_hosted_zone_id(client, zone_name):
    zones = client.list_hosted_zones_by_name(DNSName=zone_name.rstrip('.'))
    for zone in zones['HostedZones']:
        if zone['Name'].rstrip('.') == zone_name.rstrip('.'):
            return zone['Id'].split('/')[-1]
    raise Exception(f"Hosted zone for {zone_name} not found.")

def update_dns_record(client, zone_id, fqdn, ip):
    print(f"Updating {fqdn} → {ip}")
    change_batch = {
        "Comment": "DDNS update",
        "Changes": [
            {
                "Action": "UPSERT",
                "ResourceRecordSet": {
                    "Name": fqdn,
                    "Type": "A",
                    "TTL": TTL,
                    "ResourceRecords": [{"Value": ip}]
                }
            }
        ]
    }
    client.change_resource_record_sets(
        HostedZoneId=zone_id,
        ChangeBatch=change_batch
    )

def get_current_dns_ip(client, zone_id, fqdn):
    records = client.list_resource_record_sets(
        HostedZoneId=zone_id,
        StartRecordName=fqdn,
        StartRecordType="A",
        MaxItems="1"
    )["ResourceRecordSets"]
    if records and records[0]["Name"].rstrip('.') == fqdn:
        return records[0]["ResourceRecords"][0]["Value"]
    return None

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

