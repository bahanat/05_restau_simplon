from typing import Optional
from enum import Enum
from pydantic import BaseModel, ConfigDict
from datetime import datetime

from .detail import DetailsCreate, DetailsRead, DetailsUpdate


class StatusEnum(str, Enum):
    en_attente = "en_attente"
    en_preparation = "en_preparation"
    prete = "prete"
    servie = "servie"


class CommandeBase(BaseModel):
    client_id: int
    date_commande: Optional[datetime] = None
    statut: Optional[StatusEnum] = StatusEnum.en_attente
    montant_total: Optional[float] = None


class CommandeCreate(CommandeBase):
    details: list[DetailsCreate]


class CommandeRead(CommandeBase):
    id: int
    details: list[DetailsRead]

    model_config = ConfigDict(from_attributes=True)


class CommandeUpdate(BaseModel):
    client_id: Optional[int] = None
    date_commande: Optional[datetime] = None
    statut: Optional[StatusEnum] = None
    details: Optional[list[DetailsUpdate]] = None
