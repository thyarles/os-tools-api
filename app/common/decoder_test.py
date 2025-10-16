from app.common.decoder import decode_text

def test_decode_utf8_success():
    original = "hello ✓"
    data = original.encode("utf-8")
    assert decode_text(data) == original


def test_decode_falls_back_to_latin1_when_utf8_fails():
    # 0xe9 is invalid UTF-8 start byte alone, but valid latin-1 (é)
    data = bytes([0xE9])
    assert decode_text(data) == "é"


def test_decode_uses_cp1252_if_others_fail_but_cp1252_succeeds():
    class FakeContent:
        def decode(self, encoding, errors="strict"):
            # simulate failures for utf-8, latin-1 and ISO-8859-1
            if encoding.lower() == "cp1252":
                return "from-cp1252"
            raise UnicodeDecodeError(encoding, b"", 0, 1, "fail")

    assert decode_text(FakeContent()) == "from-cp1252"


def test_decode_uses_final_latin1_with_errors_ignore_if_cp1252_fails():
    class FakeContent:
        def decode(self, encoding, errors="strict"):
            # all strict decodes fail
            if errors != "strict" and encoding.lower() == "latin-1":
                return "final-ignored"
            raise UnicodeDecodeError(encoding, b"", 0, 1, "fail")

    assert decode_text(FakeContent()) == "final-ignored"