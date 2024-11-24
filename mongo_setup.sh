#!/bin/bash

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
