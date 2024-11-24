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

# Initialize the config server replica set
echo "Initializing config server replica set..."
docker exec -it configs1 mongosh --eval '
rs.initiate({
  _id: "cfgrs",
  configsvr: true,
  members: [
    { _id: 0, host: "configs1:27017" },
    { _id: 1, host: "configs2:27017" },
    { _id: 2, host: "configs3:27017" }
  ]
});
exit;
'

# Initialize the shard replica set
echo "Initializing shard replica set..."
docker exec -it mongo-us-east mongosh --eval '
rs.initiate({
  _id: "shard1rs",
  members: [
    { _id: 0, host: "mongo-us-east:27017" },
    { _id: 1, host: "mongo-us-west:27017" },
    { _id: 2, host: "mongo-us-central:27017" }
  ]
});
exit;
'

# Configure the mongos router
echo "Configuring the mongos router..."
docker exec -it mongos mongosh --eval '
sh.addShard("shard1rs/mongo-us-east:27017,mongo-us-west:27017,mongo-us-central:27017");
sh.enableSharding("scm");
sh.shardCollection("scm.orders", { region: 1 });

sh.addShardToZone("shard1rs", "us-east");
sh.updateZoneKeyRange(
  "scm.orders",
  { region: 1 },
  { region: 2 },
  "us-east"
);

sh.addShardToZone("shard1rs", "us-west");
sh.updateZoneKeyRange(
  "scm.orders",
  { region: 2 },
  { region: 3 },
  "us-west"
);

sh.addShardToZone("shard1rs", "us-central");
sh.updateZoneKeyRange(
  "scm.orders",
  { region: 3 },
  { region: Infinity },
  "us-central"
);
'

echo "MongoDB sharded cluster setup completed!"
