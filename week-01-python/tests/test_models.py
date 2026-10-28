import pytest
from pydantic import ValidationError

from extractor import Invoice


def test_valid_invoice_is_normalized():
    inv = Invoice(vendor="  Sharma Traders ", total=100, currency="inr")
    assert inv.vendor == "Sharma Traders"
    assert inv.currency == "INR"


def test_negative_total_rejected():
    with pytest.raises(ValidationError):
        Invoice(vendor="A", total=-1, currency="INR")


def test_empty_vendor_rejected():
    with pytest.raises(ValidationError):
        Invoice(vendor="   ", total=1, currency="INR")


@pytest.mark.parametrize("bad", ["RS", "RUPEES", "12$", ""])
def test_bad_currency_rejected(bad):
    with pytest.raises(ValidationError):
        Invoice(vendor="A", total=1, currency=bad)
