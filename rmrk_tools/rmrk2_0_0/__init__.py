from __future__ import annotations

import json
import urllib.parse
from dataclasses import dataclass
from enum import Enum
from typing import Any, Final, List, Optional, Union

PREFIX: Final = "RMRK"
VERSION: Final = "2.0.0"


class OP_TYPES(Enum):
    BUY = "BUY"
    LIST = "LIST"
    CREATE = "CREATE"
    MINT = "MINT"
    SEND = "SEND"
    EMOTE = "EMOTE"
    CHANGEISSUER = "CHANGEISSUER"
    BURN = "BURN"
    BASE = "BASE"
    EQUIPPABLE = "EQUIPPABLE"
    THEMEADD = "THEMEADD"
    RESADD = "RESADD"
    ACCEPT = "ACCEPT"
    EQUIP = "EQUIP"
    SETPROPERTY = "SETPROPERTY"
    LOCK = "LOCK"
    SETPRIORITY = "SETPRIORITY"


@dataclass
class MutationOp:
    op_type: OP_TYPES
    condition: Optional[str] = None


@dataclass
class Mutation:
    allowed: bool
    with_: Optional[MutationOp] = None


@dataclass
class Attribute:
    type: Union[list, dict, int, float, str]
    value: Any
    mutation: Optional[Mutation] = None


Properties = dict[str, Attribute]
Reactionmap = dict[str, list[str]]


@dataclass
class Change:
    field: str
    old: Any
    new: Any
    caller: str
    block: int
    op_type: OP_TYPES


@dataclass
class NFTChild:
    id_: str
    equipped: str
    pending: bool


Theme = dict[str, Union[str, bool]]


@dataclass
class ResourceConsolidated:
    id_: str
    pending: bool
    base: Optional[str] = None
    parts: Optional[list[str]] = None
    src: Optional[str] = None
    thumb: Optional[str] = None
    metadata: Optional[str] = None
    slot: Optional[str] = None
    theme: Optional[Theme] = None
    themeId: Optional[str] = None


@dataclass
class NFTInstanceConf:
    block: int
    collection: str
    symbol: str
    transferable: int
    sn: str
    metadata: Optional[str] = None
    owner: Optional[str] = None
    properties: Optional[Properties] = None


class NFT:
    block: int
    collection: str
    symbol: str
    transferable: int
    sn: str
    forsale: int
    reactions: Reactionmap
    priority: list[str]
    owner: str
    rootowner: str
    burned: str
    pending: bool
    metadata: Optional[str] = None
    properties: Optional[Properties] = None
    changes: list[Change] = []
    children: list[NFTChild] = []
    resources: list[ResourceConsolidated] = []

    def __init__(self, conf: NFTInstanceConf) -> None:
        self.block: Final[int] = conf.block
        self.collection: Final[str] = conf.collection
        self.symbol = conf.symbol
        self.transferable = conf.transferable
        self.sn = conf.sn
        self.resources = []
        self.metadata = conf.metadata
        self.priority = []
        self.children = []
        self.owner = conf.owner or ""
        self.rootowner = ""
        self.reactions = Reactionmap()
        self.forsale = 0
        self.burned = ""
        self.properties = conf.properties or None
        self.pending = False

    def get_id(self) -> str:
        if not self.block:
            raise Exception("not minted yet")
        return f"{self.block}-{self.collection}-{self.symbol}-{self.sn}"

    def add_change(self, change: Change) -> "NFT":
        self.changes.append(change)
        return self

    def mint(self, recipient: Optional[str] = None) -> str:
        if self.block:
            raise Exception("this NFT already minted")
        url = urllib.parse.quote(
            json.dumps(
                {
                    "collection": self.collection,
                    "symbol": self.symbol,
                    "transferable": self.transferable,
                    "sn": self.sn,
                    "metadata": self.metadata,
                    "properties": self.properties,
                }
            ),
            safe="~()*!.'",
        )
        end = ("::" + recipient.replace(r"\s", "")) if recipient else ""
        return f"{PREFIX}::{OP_TYPES.MINT.value}::{VERSION}::{url}" + end

    def send(self, recipient: str) -> str:
        if not self.block:
            raise Exception("the NFT does not exists")
        return NFT.send_by_id(self.get_id(), recipient)

    @classmethod
    def send_by_id(cls, id_: str, recipient: str) -> str:
        recipient = recipient.replace(r"\s", "")
        return f"{PREFIX}::{OP_TYPES.SEND.value}::{VERSION}::{id_}::{recipient}"

    @classmethod
    def list_by_id(cls, id_: str, price: Union[int, float]) -> str:
        return (
            f"{PREFIX}::{OP_TYPES.LIST.value}::{VERSION}::{id_}::"
            f"{price if price > 0 else 0}"
        )

    @classmethod
    def burn_by_id(cls, id_: str) -> str:
        return f"{PREFIX}::{OP_TYPES.BURN.value}::{VERSION}::{id_}"

    @classmethod
    def from_remark(cls, remark: str, block: int = 0) -> Union[NFT, str]:
        ...

    def list(self, price: Union[int, float]) -> str:
        ...

    def buy(self, recipient: Optional[str] = None) -> str:
        ...


@dataclass
class NFTMetadata:
    external_url: Optional[str] = None
    image: Optional[str] = None
    image_data: Optional[str] = None
    description: Optional[str] = None
    name: Optional[str] = None
    properties: Optional[Properties] = None


class Collection:
    block: int
    max_: int
    issuer: str
    symbol: str
    id_: str
    metadata: str
    changes: List[Change] = []
    count = 0

    def __init__(
        self,
        block: int,
        max_: int,
        issuer: str,
        symbol: str,
        id_: str,
        metadata: str,
    ):
        self.block = block
        self.max_ = max_
        self.issuer = issuer
        self.symbol = symbol
        self.id_ = id_
        self.metadata = metadata

    def create(self) -> str:
        if self.block:
            raise Exception("already created")
        url = urllib.parse.quote(
            json.dumps(
                {
                    "max": self.max_,
                    "issuer": self.issuer,
                    "symbol": self.symbol,
                    "id": self.id_,
                    "metadata": self.metadata,
                },
                separators=(",", ":"),
            ),
            safe="~()*!.'",
        )
        return f"{PREFIX}::{OP_TYPES.CREATE.value}::{VERSION}::{url}"

    @classmethod
    def generate_id(cls, pubkey: str, symbol: str) -> str:
        if not pubkey.startswith("0x"):
            raise Exception("pubkey should start with 0x")
        return pubkey[2:11] + pubkey[:-8] + "-" + symbol.upper()
