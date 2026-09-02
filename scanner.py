import socket
import time
from concurrent.futures import ThreadPoolExecutor


def scan_port(target, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.5)

    result = sock.connect_ex((target, port))
    sock.close()

    if result == 0:
        try:
            service = socket.getservbyport(port, "tcp")
        except OSError:
            service = "Unknown"

        return port, service

    return None


target = input("Enter target IP or hostname: ")

start_port = int(input("Enter starting port: "))
end_port = int(input("Enter ending port: "))

print(f"\nScanning {target} from port {start_port} to {end_port}...\n")

start_time = time.time()

open_ports = []

with ThreadPoolExecutor(max_workers=100) as executor:
    results = executor.map(
        lambda port: scan_port(target, port),
        range(start_port, end_port + 1)
    )

    for result in results:
        if result:
            open_ports.append(result)

end_time = time.time()
scan_time = end_time - start_time


print("\nOpen Ports")
print("-" * 35)

for port, service in open_ports:
    print(f"[+] {port}/tcp OPEN → {service}")


print("\nScan Summary")
print("-" * 35)
print(f"Target: {target}")
print(f"Ports scanned: {end_port - start_port + 1}")
print(f"Open ports: {len(open_ports)}")
print(f"Scan time: {scan_time:.2f} seconds")

print("\nScan complete.")