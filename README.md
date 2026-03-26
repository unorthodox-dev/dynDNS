# Dynamic DNS Manager

## Configuring the IAM in AWS

1. Go to AWS Console
2. Select IAM -> Users -> Create Users
3. Name it dyn_dns
4. Access Time, choose "Access Key - Programmatic Access"
5. Click Next, then Attach Permissions. Create a Custom Policy.
6. Select the JSON tab in the permissions window.
7. Paste the following Policy

```JSON
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

8. Name the Policy the same as the user, dyn_dns
9. Once the user is created, select it then go to the Security Credentials Tab.
10. Create an Access Key. It will only show you the access key, and secret access key once so save it somewhere.
11. Next you will install aws onto your system
12. Run AWS Configure, and input your secret, and us-east-1, and json.

## Install AWS

```
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
aws --version
```

## Configure AWS

```
aws configure
```

## Build

```
docker build -t unorthodoxdev-aws-dyndns .
```

## Run

```
docker run --rm \
  -e DDNS_DOMAIN="home.unorthodoxdev.net" \
  -e DDNS_ZONE_NAME="unorthodoxdev.net" \
  -e DDNS_TTL="300" \
  -v "$HOME/.aws:/home/appuser/.aws:ro" \
  unorthodoxdev-aws-dyndns
```
