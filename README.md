# Python TCP Port Scanner

A lightweight and multithreaded TCP port scanner built with Python for learning network security concepts and understanding how TCP ports, services, and basic service fingerprinting work.

The scanner supports configurable port ranges, concurrent scanning, service detection, HTTP fingerprinting, progress tracking, scan statistics, and CSV/JSON report generation.

## Features

- Scan a specified IP address or hostname
- Specify a custom port range
- Detect open TCP ports
- Multithreaded scanning for faster performance
- Configurable number of threads
- Configurable socket timeout
- Identify standard services associated with open ports
- Basic banner detection
- HTTP service detection on arbitrary ports
- HTTP status fingerprinting
- HTTP `Server` header detection
- Real-time scan progress indicator
- Scan duration measurement
- Professional scan summary
- Export results to CSV
- Export results to JSON
- Detailed scan metadata in JSON reports
- Input validation and error handling
- Command-line interface
- No external Python dependencies

## Technologies

- Python 3
- Socket Programming
- TCP/IP
- `concurrent.futures`
- Git & GitHub

## Requirements

- Python 3.10+
- Windows, Linux, or macOS

No external Python packages are required.

## Installation

Clone the repository:

```bash
git clone https://github.com/Mwamtindi/port-scanner.git
cd port-scanner
```

## Usage

### Interactive Mode

Run:

```bash
python scanner.py
```

The scanner will prompt you for:

```text
Enter target IP or hostname:
Enter starting port:
Enter ending port:
```

### Command-Line Mode

You can also provide the scan configuration directly through command-line arguments.

Example:

```bash
python scanner.py --target 127.0.0.1 --start 1 --end 1000 --threads 200
```

### Available Options

| Option | Description | Example |
|---|---|---|
| `--target` | Target IP address or hostname | `--target 127.0.0.1` |
| `--start` | Starting port | `--start 1` |
| `--end` | Ending port | `--end 1000` |
| `--threads` | Number of scanning threads | `--threads 200` |
| `--timeout` | Socket timeout in seconds | `--timeout 0.5` |
| `--output` | Save results to CSV or JSON | `--output scan.json` |

View all available options:

```bash
python scanner.py --help
```

## Example

Command:

```bash
python scanner.py --target 127.0.0.1 --start 1 --end 1000 --threads 200
```

Example output:

```text
Scanning 127.0.0.1 from port 1 to 1000...
Threads: 200
Timeout: 0.5 seconds

Progress: 1000/1000 (100%)

Open Ports
------------------------------------------------------------
[+] 135/tcp OPEN → epmap
    Banner: -

[+] 445/tcp OPEN → microsoft-ds
    Banner: -

Scan Summary
-----------------------------------
Target: 127.0.0.1
Ports scanned: 1000
Open ports: 2
Scan time: 2.77 seconds

Scan complete.
```

## HTTP Fingerprinting

The scanner can identify HTTP services even when they are running on non-standard ports.

For example, if a local HTTP server is running on port `3127`:

```text
[+] 3127/tcp OPEN → http
    Banner: HTTP/1.0 200 OK
    Server: SimpleHTTP/0.6 Python/3.13.15
```

The scanner sends an HTTP `HEAD` request to an open port and analyzes the response to identify HTTP status information and the `Server` header.

## Report Generation

Scan results can be exported to CSV or JSON.

### CSV

```bash
python scanner.py --target 127.0.0.1 --start 1 --end 1000 --threads 200 --output scan.csv
```

CSV reports contain:

```text
port,protocol,state,service,banner,server
135,tcp,open,epmap,,
445,tcp,open,microsoft-ds,,
```

### JSON

```bash
python scanner.py --target 127.0.0.1 --start 1 --end 1000 --threads 200 --output scan.json
```

JSON reports include scan metadata such as:

```json
{
    "target": "127.0.0.1",
    "scan_start": "2026-09-04T16:06:35.496303",
    "scan_end": "2026-09-04T16:06:38.287116",
    "start_port": 1,
    "end_port": 1000,
    "threads": 200,
    "timeout": 0.5,
    "ports_scanned": 1000,
    "open_ports": 2,
    "scan_time": 2.79,
    "results": []
}
```

Generated CSV and JSON reports are excluded from Git using `.gitignore`.

## How It Works

The scanner creates a TCP socket for each port and attempts to establish a connection.

If the connection succeeds, the port is considered open. The scanner then attempts to identify the associated service and perform basic fingerprinting.

### Basic Workflow

```text
Target
   ↓
Port Range
   ↓
Create TCP Socket
   ↓
Attempt TCP Connection
   ↓
Connection Successful?
   ├── No  → Port Closed/Filtered
   │
   └── Yes
        ↓
   Identify Service
        ↓
   Detect HTTP
        ↓
   Fingerprint Service
        ↓
   Store Result
        ↓
   Generate Summary/Report
```

## Multithreading

The scanner uses Python's `ThreadPoolExecutor` to scan multiple ports concurrently.

For example:

```bash
python scanner.py --target 127.0.0.1 --start 1 --end 1000 --threads 200
```

Increasing the number of threads can significantly reduce scanning time, especially when many ports are closed or filtered.

The scanner limits the number of threads to a maximum of `500`.

## Input Validation

The scanner validates user input before starting a scan.

Examples of validation include:

- Ports must be between `1` and `65535`
- Starting port cannot be greater than ending port
- Threads must be between `1` and `500`
- Timeout must be greater than `0`
- Output files must use `.csv` or `.json`

## Project Structure

```text
port-scanner/
│
├── scanner.py
├── README.md
├── requirements.txt
└── .gitignore
```

## Future Improvements

- [ ] UDP port scanning
- [ ] More advanced service fingerprinting
- [ ] OS detection
- [ ] Common vulnerability checks
- [ ] Custom port/service database
- [ ] Scan multiple targets
- [ ] Optional stealth scanning techniques
- [ ] Richer terminal output
- [ ] Unit and integration tests

## Security & Ethical Use

This project is intended for educational purposes and authorized security testing only.

Only scan systems, devices, and networks that you own or have explicit permission to test.

Unauthorized port scanning may violate organizational policies, terms of service, or applicable laws.

## Author

**Mwamtindi**

GitHub: https://github.com/Mwamtindi
