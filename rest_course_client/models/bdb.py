from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.bdb_type import BDBType

T = TypeVar("T", bound="BDB")


@attr.s(auto_attribs=True)
class BDB:
    """
    Attributes:
        uid (int):
        name (str):
        memory_size (int):
        type (BDBType): An enumeration.
    """

    uid: int
    name: str
    memory_size: int
    type: BDBType
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        uid = self.uid
        name = self.name
        memory_size = self.memory_size
        type = self.type.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uid": uid,
                "name": name,
                "memory_size": memory_size,
                "type": type,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        uid = d.pop("uid")

        name = d.pop("name")

        memory_size = d.pop("memory_size")

        type = BDBType(d.pop("type"))

        bdb = cls(
            uid=uid,
            name=name,
            memory_size=memory_size,
            type=type,
        )

        bdb.additional_properties = d
        return bdb

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
