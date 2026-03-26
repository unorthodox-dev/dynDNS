# Dynamic DNS Manager

This project is a simple Dynamic DNS (DDNS) updater for AWS Route53.

It checks your current public IP address and compares it to an existing DNS A record. If the IP has changed, it updates the record automatically. If nothing has changed, it does nothing.

This is useful if you are running services from a home network or any environment where your public IP changes over time.

---

## Quick Start

Once everything is configured, you can start it with:

```bash
docker compose up --build
````

The container will:

* Check your public IP
* Look up the current DNS record in Route53
* Update it only if needed

---

## AWS Setup

### Create IAM User

1. Go to AWS Console
2. Navigate to IAM → Users → Create User
3. Name it `dyn_dns`
4. Enable **Programmatic Access**
5. Continue to permissions

---

### Create Policy

Use this policy:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "route53:ListHostedZonesByName",
        "route53:ListResourceRecordSets",
        "route53:ChangeResourceRecordSets"
      ],
      "Resource": "*"
    }
  ]
}
```

Attach it to the user.

---

### Create Access Key

* Open the user → Security Credentials
* Create an access key
* Save the key and secret (you won’t see them again)

---

## Install AWS CLI

```bash
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
```

---

## Configure AWS

```bash
aws configure
```

Provide:

* Access Key
* Secret Key
* Region: `us-east-1`
* Output: `json`

This creates `~/.aws/credentials`, which the container will use.

---

## Running

Modify the docker-compose.yaml to contain your zone information.

```bash
docker compose up --build
```

---

## How It Works

* Gets your public IP from an external service
* Queries Route53 for the current A record
* Compares the values
* Updates the record if the IP has changed

This avoids unnecessary updates and keeps DNS in sync with your network.

---

## Notes

* Your domain must be managed in Route53
* `DDNS_ZONE_NAME` must match your hosted zone
* `DDNS_DOMAIN` must exist or be valid within that zone

---
