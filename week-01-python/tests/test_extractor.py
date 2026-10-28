from types import SimpleNamespace

import extractor


def fake_chat_factory(outputs):
    it = iter(outputs)

    def fake_chat(**kwargs):
        return SimpleNamespace(message=SimpleNamespace(content=next(it)))

    return fake_chat


GOOD = '{"vendor": "A", "total": 5, "currency": "INR"}'
BAD = '{"vendor": "A", "total": -5, "currency": "INR"}'


def test_success_first_try(monkeypatch):
    monkeypatch.setattr(extractor, "chat", fake_chat_factory([GOOD]))
    assert extractor.extract_invoice("x").total == 5


def test_retries_after_invalid_output(monkeypatch):
    monkeypatch.setattr(extractor, "chat", fake_chat_factory([BAD, GOOD]))
    assert extractor.extract_invoice("x").total == 5


def test_returns_none_after_all_attempts_fail(monkeypatch):
    monkeypatch.setattr(extractor, "chat", fake_chat_factory([BAD, BAD, BAD]))
    assert extractor.extract_invoice("x") is None
