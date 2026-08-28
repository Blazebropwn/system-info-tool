from sysinfo import format_text


def test_format_text_handles_nested_sections():
    sample = {
        "system": {"system": "TestOS"},
        "disk": {"disk0": {"usage_percent": 50}},
    }
    output = format_text(sample)
    assert "=== SYSTEM ===" in output
    assert "TestOS" in output
    assert "disk0:" in output
    assert "usage_percent: 50" in output
