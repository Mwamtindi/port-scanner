# Python TCP Port Scanner

A lightweight TCP port scanner built with Python for learning network security concepts and understanding how TCP ports and services work.

## Features

- Scan a specified IP address or hostname
- Specify a custom port range
- Detect open TCP ports
- Identify standard services associated with open ports
- Simple command-line interface
- No external Python dependencies

## Technologies

- Python 3
- Socket Programming
- TCP/IP
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

Run the scanner:

```bash
python scanner.py
```

You will be prompted to enter:

```text
Enter target IP or hostname:
Enter starting port:
Enter ending port:
```

### Example

```text
Enter target IP or hostname: 127.0.0.1
Enter starting port: 440
Enter ending port: 450

Scanning 127.0.0.1 from port 440 to 450...

[+] Port 445 is OPEN → microsoft-ds

Scan complete.
```

## How It Works

The scanner creates a TCP socket and attempts to establish a connection to each port in the selected range.

If the connection succeeds, the port is reported as open. For open ports, Python's built-in service database is used to display the standard service name when available.

### Basic Workflow

```text
Target
  ↓
Port Range
  ↓
Create TCP Socket
  ↓
Attempt Connection
  ↓
Connection Successful?
  ├── Yes → Port OPEN → Identify Standard Service
  └── No  → Port CLOSED/FILTERED
```

## Project Structure

```text
port-scanner/
├── scanner.py
├── README.md
├── requirements.txt
└── .gitignore
```

## Future Improvements

- [ ] Multithreaded scanning
- [ ] Improved service/banner detection
- [ ] Scan progress indicator
- [ ] Command-line arguments
- [ ] Scan duration measurement
- [ ] CSV report generation
- [ ] Better error handling
- [ ] Configurable timeout
- [ ] Professional scan summary

## Security & Ethical Use

This project is intended for educational purposes and authorized security testing only.

Only scan systems, devices, and networks that you own or have explicit permission to test.

Unauthorized port scanning may violate organizational policies, terms of service, or applicable laws.

## Author

**Mwamtindi**

GitHub: https://github.com/Mwamtindi
