from pydantic import BaseModel
from typing import Optional, Literal

class Phone(BaseModel):
    number: str
    source: Literal["whatsapp", "viber", "telegram"]
    created_at: Optional[str]