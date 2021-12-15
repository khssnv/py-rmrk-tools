import json
import urllib.parse
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Final, Literal, Optional, Union

PREFIX: Final = "RMRK"
VERSION: Final = "1.0.0"


class OP_TYPES(Enum):
    BUY = "BUY"
    LIST = "LIST"
    MINT = "MINT"
    MINTNFT = "MINTNFT"
    SEND = "SEND"
    EMOTE = "EMOTE"
    CHANGEISSUER = "CHANGEISSUER"
    CONSUME = "CONSUME"


DisplayType = Literal[
    "boost_number",
    "boost_percentage",
    "number",
    "date",
]


@dataclass
class Attribute:
    display_type: Optional[DisplayType]
    trait_type: Optional[str]
    value: Union[float, str]
    max_value: Optional[float]


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
class NFTMetadata:
    external_url: Optional[str] = None
    image: Optional[str] = None
    image_data: Optional[str] = None
    description: Optional[str] = None
    name: Optional[str] = None
    attributes: list[Attribute] = field(default_factory=list)
    background_color: Optional[str] = None
    animation_url: Optional[str] = None
    youtube_url: Optional[str] = None


class NFT:
    updatedAtBlock: Optional[int]
    loadedMetadata: Optional[NFTMetadata]
    forsale: int = 0
    reactions: Reactionmap = Reactionmap()
    changes: list[Change] = []
    owner: str = ""
    burned: str = ""

    def __init__(
        self,
        block: int,
        collection: str,
        name: str,
        instance: str,
        transferable: int,
        sn: str,
        metadata: Optional[str] = None,
        data: Optional[str] = None,
        updatedAtBlock: Optional[int] = None,
    ) -> None:
        self._block: Final[int] = block
        self._collection: Final[str] = collection
        self._name: Final[str] = name
        self._instance: Final[str] = instance
        self._transferable: Final[int] = transferable
        self._sn: Final[sn] = sn
        self._data: str = data
        self._metadata: str = metadata
        self.updatedAtBlock = updatedAtBlock or block

    @property
    def block(self) -> int:
        return self._block

    @property
    def collection(self) -> str:
        return self._collection

    @property
    def name(self) -> str:
        return self._name

    @property
    def instance(self) -> str:
        return self._instance

    @property
    def transferable(self) -> int:
        return self._transferable

    @property
    def data(self) -> Optional[str]:
        return self._data

    @property
    def sn(self) -> str:
        return self._sn

    @property
    def metadata(self) -> Optional[str]:
        return self._metadata

    def get_id(self) -> str:
        if not self.block:
            raise Exception("not minted yet")
        return f"{self.block}-{self.collection}-{self.instance}-{self.sn}"

    def add_change(self, change: Change) -> "NFT":
        self.changes.append(change)
        return self

    def mintnft(self) -> str:
        if self.block:
            raise Exception("this NFT is already minted")
        uri = urllib.parse.quote(
            json.dumps(
                {
                    "collection": self.collection,
                    "name": self.name,
                    "instance": self.instance,
                    "transferable": self.transferable,
                    "sn": self.sn,
                    "metadata": self.metadata,
                }
            ),
            safe="~()*!.'",
        )
        return f"{PREFIX}::{OP_TYPES.MINTNFT.value}::{VERSION}::{uri}"

    def send(self, recipient: str) -> str:
        if not self.block:
            raise Exception("the NFT does not exists")
        recipient = recipient.replace(r"\s", "")
        return (
            f"{PREFIX}::${OP_TYPES.SEND.value}::{VERSION}::{self.get_id()}::{recipient}"
        )
