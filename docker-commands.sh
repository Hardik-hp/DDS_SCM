#!/bin/bash

# Ensure the script exits on any error
set -e

# Create certificates directory
mkdir -p certs
docker-compose up -d

# Generate CA certificate
docker run -it --rm -v "$(pwd)/certs:/certs" cockroachdb/cockroach cert create-ca \
    --certs-dir=/certs --ca-key=/certs/ca.key

# Generate node certificates
docker run -it --rm -v "$(pwd)/certs:/certs" cockroachdb/cockroach cert create-node \
    cockroach-us-east \
    cockroach-us-west \
    cockroach-us-central \
    localhost \
    127.0.0.1 \
    --certs-dir=/certs --ca-key=/certs/ca.key

# Generate client certificate for root user
docker run -it --rm -v "$(pwd)/certs:/certs" cockroachdb/cockroach cert create-client root \
    --certs-dir=/certs --ca-key=/certs/ca.key

# Initialize the cluster
docker exec -it cockroach-us-east ./cockroach init \
    --certs-dir=/cockroach/certs \
    --host=cockroach-us-east

# Check if license_key.txt exists
if [ ! -f license_key.txt ]; then
  echo "Error: license_key.txt file not found."
  exit 1
fi

# Read the license key from the file
LICENSE_KEY=$(cat license_key.txt)

# Set cluster settings
docker exec -i cockroach-us-east ./cockroach sql \
    --certs-dir=/cockroach/certs \
    --host=cockroach-us-east <<EOF
SET CLUSTER SETTING cluster.organization = 'Arizona State University';
SET CLUSTER SETTING enterprise.license = '${LICENSE_KEY}';
CREATE USER dds_user WITH PASSWORD 'admin';
GRANT admin TO dds_user;
EOF
