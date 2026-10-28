import sys
import time

from ollama import chat
from pydantic import BaseModel, ValidationError

MODEL = sys.argv[1] if len(sys.argv) > 1 else "qwen3.5:4b"
MAX_ATTEMPTS = 3


class Invoice(BaseModel):
    vendor: str
    total: float
    currency: str


PROMPT = (
    "Extract vendor, total (number only) and ISO currency code from this text. "
    "Correct obvious typos in the vendor name and use proper capitalization. "
    "The total is the final amount due for THIS invoice only. Do not include subtotals, advances or previous balances.\n\n{text}"
)


def extract_invoice(text: str) -> Invoice | None:
    for attempt in range(1, MAX_ATTEMPTS + 1):
        start = time.time()
        response = chat(
            model=MODEL,
            messages=[{"role": "user", "content": PROMPT.format(text=text)}],
            format=Invoice.model_json_schema(),
            think=False,
            options={"temperature": 0},
        )
        elapsed = time.time() - start
        try:
            invoice = Invoice.model_validate_json(response.message.content)
            print(f"  attempt {attempt} OK in {elapsed:.1f}s")
            return invoice
        except ValidationError as e:
            print(f"  attempt {attempt} failed in {elapsed:.1f}s: {e}")
    return None


# Mini test set: (input text, expected output)
TESTS = [
    (
        "Invoice from Sharma Traders, total amount due Rs. 14,250.",
        Invoice(vendor="Sharma Traders", total=14250, currency="INR"),
    ),
    (
        "inv #221 sharma trdrs ... subtotal 12,000 + GST 2,250 = 14,250 INR. paid advance 5000",
        Invoice(vendor="Sharma Traders", total=14250, currency="INR"),
    ),
    (
        "gupta dairy - milk 10 x 450 = 4500 - GST 5% 225 - grand total Rs 4,725",
        Invoice(vendor="Gupta Dairy", total=4725, currency="INR"),
    ),
    (
        "Bill from Patel Hardware. Total payable: Rs 1,20,500 (one lakh twenty thousand five hundred).",
        Invoice(vendor="Patel Hardware", total=120500, currency="INR"),
    ),
    (
        "Receipt: Fresh Mart, USD 89.99 paid by card",
        Invoice(vendor="Fresh Mart", total=89.99, currency="USD"),
    ),
    (
        "Invoice no 77 from kumar electricals. Amount: 8,400/-",
        Invoice(vendor="Kumar Electricals", total=8400, currency="INR"),
    ),
    (
        "om sai stores bill. items 1,800 + GST 18% 324 = 2,124. Previous balance 5,000 not included.",
        Invoice(vendor="Om Sai Stores", total=2124, currency="INR"),
    ),
]

print(f"Model: {MODEL}\n")
passed = 0
for i, (text, expected) in enumerate(TESTS, start=1):
    print(f"Test {i}:")
    result = extract_invoice(text)
    ok = result == expected
    passed += ok
    print(f"  got:      {result}")
    print(f"  expected: {expected}")
    print(f"  {'PASS' if ok else 'FAIL'}")

print(f"\n[{MODEL}] Score: {passed}/{len(TESTS)}")
