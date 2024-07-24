from typing import Optional, Union

from bw2data.backends import SQLiteBackend, Activity
from bw2data.configuration import TypoSettings
# from bw2data.backends.typos import VALID_EXCHANGE_TYPES, VALID_ACTIVITY_TYPES
from pydantic import BaseModel, field_validator, Field

_bw_types = TypoSettings()

class ExchangeModel(BaseModel):
    input: str
    output: str
    type: str
    amount: float

    @field_validator("type", mode="before")
    @classmethod
    def validate_type(cls, type_: str):
        if type_ not in _bw_types.edge_types:
            raise ValueError(f"Invalid exchange type: {type_}")
        return type_


class ActivityModel(BaseModel):
    name: str
    code: str
    type: str
    unit: str
    category: Optional[list[str]] = None
    location: Optional[str] = None

    # exchanges: list[ExchangeModel]

    @field_validator("type", mode="before")
    @classmethod
    def validate_type(cls, type_: str):
        if type_ not in _bw_types.node_types:
            raise ValueError(f"Invalid activity type: {type_}")
        return type_


class DBData(BaseModel):
    activities: list[ActivityModel]
    exchanges: Optional[list[ExchangeModel]] = Field(default_factory=list)


def build_network(db: SQLiteBackend, data: Union[dict,DBData]):
    """
    Build activities and exchanges based on DBData structured input.
    Does not return anything
    :param db: bw2 sql activities database
    :param data: data of activities and exchanges
    """
    if isinstance(data, dict):
        data = DBData(**data)

    def create_edge(act: Activity, input: Activity, amount: float, type_: str):
        return act.new_edge(
            amount=amount,
            type=type_,
            input=input
        ).save()

    node_map: dict[str, Activity] = {}
    for activity in data.activities:
        node = db.new_node(**activity.model_dump())
        node.save()
        node_map[node["code"]] = node
    for exchange in data.exchanges:
        create_edge(node_map[exchange.input], node_map[exchange.output], exchange.amount, exchange.type)
