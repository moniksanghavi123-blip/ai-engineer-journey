from ollama import chat
from pydantic import BaseModel


class Invoice(BaseModel):
    vendor: str
    total: float
    currency: str


# FUNCTION: the recipe card.
# "text" is the ingredient we hand in each time.
def extract_invoice(text):
    response = chat(
        model="qwen3.5:4b",
        messages=[{
            "role": "user",
            "content": f"Extract vendor, total and currency. Fix typos in vendor.\n\n{text}",
        }],
        format=Invoice.model_json_schema(),
        think=False,
        options={"temperature": 0},
    )
    # RETURN: hand the finished Invoice back to whoever asked for it
    return Invoice.model_validate_json(response.message.content)


# Three different invoices (the "orders")
texts = [
    "Invoice from Sharma Traders, total amount due Rs. 14,250.",
    "gupta dairy - milk 10 x 450 = 4500 - GST 5% 225 - grand total Rs 4,725",
    "Receipt: Fresh Mart, USD 89.99 paid by card",
    "Bill from Patel Hardware. Total payable: Rs 1,20,500"
]

# LOOP: do the same thing for each text in the list
for t in texts:
    inv = extract_invoice(t)
    print(inv.vendor, "->", inv.total, inv.currency)
