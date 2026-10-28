# ---- 1. IMPORTS: tools we borrow from other people's code ----
from ollama import chat          # a function that sends text to the Ollama program on your Mac
from pydantic import BaseModel   # lets us define a "form" with rules

# ---- 2. THE FORM: the shape we want the answer in ----
class Invoice(BaseModel):
    vendor: str      # must be text
    total: float     # must be a number
    currency: str    # must be text
    invoice_number: str

# ---- 3. THE INPUT: the messy text we want to understand ----
text = "inv #221 sharma trdrs ... subtotal 12,000 + GST 2,250 = 14,250 INR. paid advance 5000"

# ---- 4. THE CALL: send the text to the model ----
response = chat(
    model="qwen3.5:4b",                       # which model to use
    messages=[{                               # the conversation so far (just one message)
        "role": "user",                       # "user" = you speaking to the model
        "content": f"Extract vendor, total and currency. Fix typos in vendor.\n\n{text}",
    }],
    format=Invoice.model_json_schema(),       # "answer in the shape of my form"
    think=False,                              # skip the model's long internal reasoning
    options={"temperature": 0},               # 0 = no randomness, same input gives same output
)

# ---- 5. THE ANSWER: the model returns text, not a Python object ----
raw = response.message.content
print("Raw text from model:", raw)
print("Type of raw:", type(raw))

# ---- 6. VALIDATE: turn that text into a real Invoice, checking the rules ----
invoice = Invoice.model_validate_json(raw)
print("Type of invoice:", type(invoice))
print("Vendor:", invoice.vendor)
print("Total + 1000 =", invoice.total + 1000)
