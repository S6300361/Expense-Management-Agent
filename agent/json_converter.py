import json
from pydantic import BaseModel

def model_to_json(model: BaseModel) -> str:
    return json.dumps(model.model_dump(mode="json"), ensure_ascii=False)
