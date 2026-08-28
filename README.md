# System Info Tool

A small cross-platform Python CLI for inspecting system metrics, exporting reports, and monitoring CPU and memory usage.

## Features

- OS and hardware information
- CPU, memory, disk, and filesystem metrics
- Hostname and local IP information
- JSON or plain-text export
- Live CPU and memory monitoring
- Windows, Linux, and macOS support

## Installation

```bash
git clone https://github.com/Blazebropwn/system-info-tool.git
cd system-info-tool
python -m venv .venv
pip install -r requirements.txt
```

## Usage

```bash
python sysinfo.py --display
python sysinfo.py --export systeminfo.json
python sysinfo.py --export report.txt
python sysinfo.py --live --interval 5
python sysinfo.py --version
```

## Development

```bash
pip install -r requirements-dev.txt
pytest
```

Built to practice practical Python, CLI design, operating-system APIs, structured data export, and defensive error handling.

## License

MIT
