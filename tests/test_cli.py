import json

import pytest

import sysinfo


SAMPLE = {"system": {"system": "TestOS"}}


def test_exports_json_and_text(tmp_path, monkeypatch):
    monkeypatch.setattr(sysinfo, "collect_system_info", lambda: SAMPLE)
    json_path = tmp_path / "report.json"
    text_path = tmp_path / "report.txt"
    sysinfo.export_to_file(str(json_path))
    sysinfo.export_to_file(str(text_path))
    assert json.loads(json_path.read_text()) == SAMPLE
    assert "TestOS" in text_path.read_text()


def test_rejects_unknown_export_extension(tmp_path):
    with pytest.raises(ValueError, match=".json or .txt"):
        sysinfo.export_to_file(str(tmp_path / "report.csv"))


def test_parser_keeps_actions_mutually_exclusive():
    parser = sysinfo.build_parser()
    with pytest.raises(SystemExit):
        parser.parse_args(["--display", "--live"])
