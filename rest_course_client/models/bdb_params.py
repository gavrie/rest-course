from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.bdb_type import BDBType
from ..types import UNSET, Unset

T = TypeVar("T", bound="BDBParams")


@attr.s(auto_attribs=True)
class BDBParams:
    """
    Attributes:
        name (str):
        memory_size (int):
        type (Union[Unset, BDBType]): An enumeration. Default: BDBType.REDIS.
    """

    name: str
    memory_size: int
    type: Union[Unset, BDBType] = BDBType.REDIS
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        memory_size = self.memory_size
        type: Union[Unset, str] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "memory_size": memory_size,
            }
        )
        if type is not UNSET:
            field_dict["type"] = type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        memory_size = d.pop("memory_size")

        _type = d.pop("type", UNSET)
        type: Union[Unset, BDBType]
        if isinstance(_type, Unset):
            type = UNSET
        else:
            type = BDBType(_type)

        bdb_params = cls(
            name=name,
            memory_size=memory_size,
            type=type,
        )

        bdb_params.additional_properties = d
        return bdb_params

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
