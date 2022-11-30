py-rmrk-tools
=============

A port of [rmrk-tools](https://github.com/rmrk-team/rmrk-tools) for Python.

Installation
------------

Python 3.9 and higher supported.

```console
pip install py-rmrk-tools
```

What's done
-----------

The package contains only those features I currently need for my other projects. But feel free to create an [issue](https://github.com/khssnv/py-rmrk-tools/issues/new) in case you want to request any other feature ported here from the [rmrk-tools](https://github.com/rmrk-team/rmrk-tools) package. Also [pull requests](https://github.com/khssnv/py-rmrk-tools/pulls) are very welcome!

### RMRK 1.0.0

- [x] Constants and enums,
- [x] Definitions: Attribute, Properties, Reactionmap, Change, NFTMetadata,
- [x] NFT entity,
- [ ] Collection entity.

### RMRK 2.0.0

- [x] Constants and enums,
- [x] Definitions: MutationOp, Mutation, Attribute, Properties, Reactionmap, Change, NFTChild, ResourceConsolidated, NFTInstanceConf, NFTMetadata,
- [x] NFT entity,
- [x] Collection entity (partially).

Who uses it
-----------

I use this package in production for a couple of projects:

* At [https://spot.merklebot.com](https://spot.merklebot.com/) it mints a RMRK NFT for each Boston Dynamics Spot robot demo launch which triggers by a `Launch` type transaction in [Robonomics Network](https://robonomics.network/) blockchain,
* At [https://telescope.merklebot.com](https://telescope.merklebot.com) it worked to produce RMRK NFTs from deep space photos made by [https://atacamascope.cl](https://atacamascope.cl/) telescope in Atacama desert, Chile.
