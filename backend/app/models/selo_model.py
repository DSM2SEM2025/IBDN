from pydantic import BaseModel, Field
from typing import List

from pydantic import BaseModel

class AssociacaoMultiplaRequest(BaseModel):
    #Associar um selo a uma empresa em uma única etapa
    id_tipo_selo: int = Field(..., description="ID do tipo de selo a ser criado e associado.")
    dias_validade: int = Field(365, description="Número de dias que o selo será válido a partir da emissão.")

    class Config:
        json_schema_extra = {
            "example": {
                "id_tipo_selo": 2,
                "dias_validade": 730
            }
        }
