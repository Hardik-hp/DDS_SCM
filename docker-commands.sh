#!/bin/bash

# Ensure the script exits on any error
set -e

# Create certificates directory
mkdir -p certs
docker-compose up -d

# Check if CA certificate exists
if [ ! -f "certs/ca.crt" ] || [ ! -f "certs/ca.key" ]; then
    echo "Generating CA certificate..."
    docker run -it --rm -v "$(pwd)/certs:/certs" cockroachdb/cockroach cert create-ca \
        --certs-dir=/certs --ca-key=/certs/ca.key
else
    echo "CA certificate already exists. Skipping CA certificate generation."
fi

# Check if node certificates exist
if [ ! -f "certs/node.crt" ] || [ ! -f "certs/node.key" ]; then
    echo "Generating node certificates..."
    docker run -it --rm -v "$(pwd)/certs:/certs" cockroachdb/cockroach cert create-node \
        cockroach-us-east \
        cockroach-us-west \
        cockroach-us-central \
        localhost \
        127.0.0.1 \
        --certs-dir=/certs --ca-key=/certs/ca.key
else
    echo "Node certificates already exist. Skipping node certificate generation."
fi

# Check if client certificate for root exists
if [ ! -f "certs/client.root.crt" ] || [ ! -f "certs/client.root.key" ]; then
    echo "Generating client certificate for root user..."
    docker run -it --rm -v "$(pwd)/certs:/certs" cockroachdb/cockroach cert create-client root \
        --certs-dir=/certs --ca-key=/certs/ca.key
else
    echo "Client certificate for root already exists. Skipping client certificate generation."
fi

# Wait until the node is ready
until docker exec -it cockroach-us-east curl --silent --fail http://cockroach-us-east:8080/health; do
    echo "Waiting for cockroach-us-east to be ready..."
    sleep 2
done

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
