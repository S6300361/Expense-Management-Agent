import json
from datetime import date
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict, field_validator

class Expense(BaseModel):
    model_config = ConfigDict(extra="allow")
    amount: float = Field(gt=0)
    currency: str = Field(min_length=3, max_length=3)
    category: str = Field(min_length=1)
    payment_method: str = Field(min_length=1)
    description: str = Field(min_length=1)
    date: date
    vendor: Optional[str] = None
    notes: Optional[str] = None

    @field_validator("currency")
    @classmethod
    def uppercase_currency(cls, value):
        return value.upper()

def validate_expense(data):
    if isinstance(data, str):
        data = json.loads(data)
    return Expense.model_validate(data)
