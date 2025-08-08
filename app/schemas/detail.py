from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class DetailsBase(BaseModel):
    produit_id: int
    quantite: int = Field(gt=0)


class DetailsCreate(DetailsBase):
    pass


class DetailsRead(DetailsBase):
    pass

    model_config = ConfigDict(from_attributes=True)


class DetailsUpdate(BaseModel):
    produit_id: Optional[int]
    quantite: Optional[int] = Field(gt=0)
