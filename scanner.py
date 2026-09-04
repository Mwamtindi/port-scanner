import socket
import time
import argparse
import csv
import json
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

def save_to_csv(filename, results):
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        writer.writerow([
            "port",
            "protocol",
            "state",
            "service",
            "banner",
            "server"
        ])

        for port, service, banner, server in results:
            writer.writerow([
                port,
                "tcp",
                "open",
                service,
                banner,
                server
            ])

def save_to_json(
    filename,
    target,
    results,
    scan_time,
    total_ports,
    scan_start,
    scan_end,
    start_port,
    end_port,
    threads,
    timeout
):
    report = {
        "target": target,
        "scan_start": scan_start,
        "scan_end": scan_end,
        "start_port": start_port,
        "end_port": end_port,
        "threads": threads,
        "timeout": timeout,
        "ports_scanned": total_ports,
        "open_ports": len(results),
        "scan_time": round(scan_time, 2),
        "results": []
    }

    for port, service, banner, server in results:
        report["results"].append({
            "port": port,
            "protocol": "tcp",
            "state": "open",
            "service": service,
            "banner": banner,
            "server": server
        })

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(report, file, indent=4)

def detect_http(sock):
    try:
        request = (
            "HEAD / HTTP/1.1\r\n"
            "Host: localhost\r\n"
            "Connection: close\r\n"
            "\r\n"
        )

        sock.sendall(request.encode())

        response = sock.recv(1024).decode(
            "utf-8",
            errors="ignore"
        )

        if response.startswith("HTTP/"):
            lines = response.splitlines()

            status = lines[0]
            server = ""

            for line in lines[1:]:
                if line.lower().startswith("server:"):
                    server = line.split(":", 1)[1].strip()
                    break

            return status, server

    except (socket.timeout, socket.error):
        pass

    return "", ""

def scan_port(target, port, timeout):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)

    try:
        result = sock.connect_ex((target, port))

        if result == 0:
            try:
                service = socket.getservbyport(port, "tcp")
            except OSError:
                service = "Unknown"

            banner = ""
            server = ""

            try:
                http_status, server = detect_http(sock)

                if http_status:
                    service = "http"
                    banner = http_status

            except (socket.timeout, socket.error):
                pass

            return port, service, banner, server

    except socket.error:
        return None

    finally:
        sock.close()

    return None


# Command-line arguments
parser = argparse.ArgumentParser(
    description="Python TCP Port Scanner"
)

parser.add_argument(
    "--target",
    required=True,
    help="Target IP address or hostname"
)

parser.add_argument(
    "--start",
    type=int,
    required=True,
    help="Starting port"
)

parser.add_argument(
    "--end",
    type=int,
    required=True,
    help="Ending port"
)

parser.add_argument(
    "--threads",
    type=int,
    default=100,
    help="Number of concurrent threads (default: 100)"
)

parser.add_argument(
    "--output",
    help="Save scan results to a CSV or JSON file (e.g., scan.csv or scan.json)"
)

parser.add_argument(
    "--timeout",
    type=float,
    default=0.5,
    help="Socket timeout in seconds (default: 0.5)"
)

args = parser.parse_args()

target = args.target
start_port = args.start
end_port = args.end
threads = args.threads
output_file = args.output
timeout = args.timeout


# Input validation
if start_port < 1 or end_port > 65535:
    parser.error("Ports must be between 1 and 65535.")

if start_port > end_port:
    parser.error("Starting port cannot be greater than ending port.")

if threads < 1 or threads > 500:
    parser.error("Threads must be between 1 and 500.")

if timeout <= 0:
    parser.error("Timeout must be greater than 0.")

if output_file:
    if not (
        output_file.lower().endswith(".csv")
        or output_file.lower().endswith(".json")
    ):
        parser.error("Output file must end with .csv or .json.")


# Start scan
print(f"\nScanning {target} from port {start_port} to {end_port}...")
print(f"Threads: {threads}\n")
print(f"Timeout: {timeout} seconds\n")

scan_start = datetime.now().isoformat()
start_time = time.time()

open_ports = []

total_ports = end_port - start_port + 1
completed = 0

with ThreadPoolExecutor(max_workers=threads) as executor:

    futures = [
        executor.submit(scan_port, target, port, timeout)
        for port in range(start_port, end_port + 1)
    ]

    for future in as_completed(futures):
        result = future.result()

        completed += 1

        if completed % 100 == 0 or completed == total_ports:
            percentage = (completed / total_ports) * 100
            print(
                f"\rProgress: {completed}/{total_ports} "
                f"({percentage:.0f}%)",
                end="",
                flush=True
            )

        if result:
            open_ports.append(result)


# Sort results by port number
open_ports.sort()


# Calculate scan time
scan_end = datetime.now().isoformat()
end_time = time.time()
scan_time = end_time - start_time


# Display results
print("\nOpen Ports")
print("-" * 60)

if open_ports:
    for port, service, banner, server in open_ports:
        print(f"[+] {port}/tcp OPEN → {service}")

        if banner:
            print(f"    Banner: {banner}")
        else:
            print("    Banner: -")

        if server:
            print(f"    Server: {server}")
else:
    print("No open ports found.")


# Display summary
print("\nScan Summary")
print("-" * 35)
print(f"Target: {target}")
print(f"Ports scanned: {end_port - start_port + 1}")
print(f"Open ports: {len(open_ports)}")
print(f"Scan time: {scan_time:.2f} seconds")

if output_file:
    if output_file.lower().endswith(".csv"):
        save_to_csv(output_file, open_ports)

    elif output_file.lower().endswith(".json"):
        save_to_json(
            output_file,
            target,
            open_ports,
            scan_time,
            end_port - start_port + 1,
            scan_start,
            scan_end,
            start_port,
            end_port,
            threads,
            timeout
        )

    print(f"\nReport saved to: {output_file}")

print("\nScan complete.")