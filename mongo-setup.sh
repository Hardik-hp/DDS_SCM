#!/bin/bash

# Ensure the script exits on any error
set -e
# Set up the Config Server
echo "Setting up Config Server Replication Set..."
docker exec config1 mongosh --port 27019 --eval 'rs.initiate({
    _id: "configReplSet",
    configsvr: true,
    members: [
        { _id: 0, host: "config1:27019" },
        { _id: 1, host: "config2:27019" },
        { _id: 2, host: "config3:27019" }
    ]
})'

# Wait for replica set to initialize
docker exec config1 mongosh --port 27019 --eval '
var checkReplStatus = function() {
    var status = rs.status();
    return status.members.some(m => m.stateStr === "PRIMARY");
};
while (!checkReplStatus()) { sleep(1000); }'

# Set up Shard for US East
echo "Setting up US East Replication Set..."
docker exec us_east_1 mongosh --port 27018 --eval 'rs.initiate({
    _id: "us_eastReplSet",
    members: [
        { _id: 0, host: "us_east_1:27018" },
        { _id: 1, host: "us_east_2:27018" },
        { _id: 2, host: "us_east_3:27018" }
    ]
})'
# Wait for replica set to initialize
docker exec us_east_1 mongosh --port 27018 --eval '
var checkReplStatus = function() {
    var status = rs.status();
    return status.members.some(m => m.stateStr === "PRIMARY");
};
while (!checkReplStatus()) { sleep(1000); }'

# Set up Shard for US West
echo "Setting up US West Replication Set..."
docker exec us_west_1 mongosh --port 27018 --eval 'rs.initiate({
    _id: "us_westReplSet",
    members: [
        { _id: 0, host: "us_west_1:27018" },
        { _id: 1, host: "us_west_2:27018" },
        { _id: 2, host: "us_west_3:27018" }
    ]
})'
# Wait for replica set to initialize
docker exec us_west_1 mongosh --port 27018 --eval '
var checkReplStatus = function() {
    var status = rs.status();
    return status.members.some(m => m.stateStr === "PRIMARY");
};
while (!checkReplStatus()) { sleep(1000); }'

# Set up Shard for US Central
echo "Setting up US Central Replication Set..."
docker exec us_central_1 mongosh --port 27018 --eval 'rs.initiate({
    _id: "us_centralReplSet",
    members: [
        { _id: 0, host: "us_central_1:27018" },
        { _id: 1, host: "us_central_2:27018" },
        { _id: 2, host: "us_central_3:27018" }
    ]
})'
# Wait for replica set to initialize
docker exec us_central_1 mongosh --port 27018 --eval '
var checkReplStatus = function() {
    var status = rs.status();
    return status.members.some(m => m.stateStr === "PRIMARY");
};
while (!checkReplStatus()) { sleep(1000); }'

# Wait for mongos to be ready
until docker exec mongos1 mongosh --host 127.0.0.1 --port 27017 --eval 'db.runCommand({ping: 1})'; do
    echo "Waiting for mongos to initialize..."
    sleep 2
done

# Set up Mongos Router and Database Sharding
# echo "Setting up Mongos Router..."
# docker exec mongos1 mongosh --host 127.0.0.1 --port 27017 --eval '
# sh.addShard("us_eastReplSet/us_east_1:27018");
# sh.addShard("us_westReplSet/us_west_1:27018");
# sh.addShard("us_centralReplSet/us_central_1:27018");

# sh.addShardToZone("us_eastReplSet", "us_east");
# sh.addShardToZone("us_westReplSet", "us_west");
# sh.addShardToZone("us_centralReplSet", "us_central");

# sh.enableSharding("scm");

# sh.shardCollection("scm.orders", { region: 1 });

# sh.updateZoneKeyRange(
#   "scm.orders",
#   { region: 1 },
#   { region: 2 },
#   "us_east"
# );
# sh.updateZoneKeyRange(
#   "scm.orders",
#   { region: 2 },
#   { region: 3 },
#   "us_west"
# );
# sh.updateZoneKeyRange(
#   "scm.orders",
#   { region: 3 },
#   { region: Infinity },
#   "us_central"
# );
# '
# echo "MongoDB Regional Sharding Setup Complete!"
