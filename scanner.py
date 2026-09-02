import socket
import time
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed


def scan_port(target, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.5)

    try:
        result = sock.connect_ex((target, port))

        if result == 0:
            try:
                service = socket.getservbyport(port, "tcp")
            except OSError:
                service = "Unknown"

            banner = ""

            try:
                sock.sendall(b"\r\n")
                banner = sock.recv(1024).decode(
                    "utf-8",
                    errors="ignore"
                ).strip()
            except (socket.timeout, socket.error):
                banner = ""

            return port, service, banner

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

args = parser.parse_args()

target = args.target
start_port = args.start
end_port = args.end
threads = args.threads


# Input validation
if start_port < 1 or end_port > 65535:
    parser.error("Ports must be between 1 and 65535.")

if start_port > end_port:
    parser.error("Starting port cannot be greater than ending port.")

if threads < 1 or threads > 500:
    parser.error("Threads must be between 1 and 500.")


# Start scan
print(f"\nScanning {target} from port {start_port} to {end_port}...")
print(f"Threads: {threads}\n")

start_time = time.time()

open_ports = []

total_ports = end_port - start_port + 1
completed = 0

with ThreadPoolExecutor(max_workers=threads) as executor:

    futures = [
        executor.submit(scan_port, target, port)
        for port in range(start_port, end_port + 1)
    ]

    for future in as_completed(futures):
        result = future.result()

        completed += 1

        if completed % 100 == 0 or completed == total_ports:
            percentage = (completed / total_ports) * 100
            print(
                f"\rProgress: {completed}/{total_ports}"
                f"({percentage:.0f}%)",
                end="",
                flush=True
            )

        if result:
            open_ports.append(result)


# Sort results by port number
open_ports.sort()


# Calculate scan time
end_time = time.time()
scan_time = end_time - start_time


# Display results
print("\nOpen Ports")
print("-" * 35)

if open_ports:
    for port, service, banner in open_ports:
        print(f"[+] {port}/tcp OPEN → {service}")

        if banner:
            print(f"    Banner: {banner}")
else:
    print("No open ports found.")


# Display summary
print("\nScan Summary")
print("-" * 35)
print(f"Target: {target}")
print(f"Ports scanned: {end_port - start_port + 1}")
print(f"Open ports: {len(open_ports)}")
print(f"Scan time: {scan_time:.2f} seconds")

print("\nScan complete.")