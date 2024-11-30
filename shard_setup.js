sh.addShard("us_eastReplSet/us_east_1:27018");
sh.addShard("us_westReplSet/us_west_1:27018");
sh.addShard("us_centralReplSet/us_central_1:27018");

sh.addShardToZone("us_eastReplSet", "us_east");
sh.addShardToZone("us_westReplSet", "us_west");
sh.addShardToZone("us_centralReplSet", "us_central");

sh.enableSharding("scm");
db.orders.createIndex({region: 1})
sh.shardCollection("scm.orders", { region: 1 });

sh.updateZoneKeyRange(
    "scm.orders",
    { region: 1 },
    { region: 2 },
    "us_east"
);
sh.updateZoneKeyRange(
    "scm.orders",
    { region: 2 },
    { region: 3 },
    "us_west"
);
sh.updateZoneKeyRange(
    "scm.orders",
    { region: 3 },
    { region: Infinity },
    "us_central"
);
