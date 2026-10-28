from ollama import chat
from pydantic import BaseModel, Field, ValidationError, field_validator

DEFAULT_MODEL = "qwen3.5:4b"
MAX_ATTEMPTS = 3

PROMPT = (
    "Extract vendor, total (number only) and ISO currency code from this text. "
    "Correct obvious typos in the vendor name and use proper capitalization. "
    "The total is the final amount due, not a subtotal or advance.\n\n{text}"
)


class Invoice(BaseModel):
    vendor: str
    total: float = Field(gt=0)
    currency: str

    @field_validator("vendor")
    @classmethod
    def clean_vendor(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("vendor is empty")
        return v

    @field_validator("currency")
    @classmethod
    def check_currency(cls, v: str) -> str:
        v = v.strip().upper()
        if len(v) != 3 or not v.isalpha():
            raise ValueError("currency must be a 3-letter code")
        return v


def extract_invoice(text: str, model: str = DEFAULT_MODEL) -> Invoice | None:
    for _ in range(MAX_ATTEMPTS):
        response = chat(
            model=model,
            messages=[{"role": "user", "content": PROMPT.format(text=text)}],
            format=Invoice.model_json_schema(),
            think=False,
            options={"temperature": 0},
        )
        try:
            return Invoice.model_validate_json(response.message.content)
        except ValidationError:
            continue
    return None
