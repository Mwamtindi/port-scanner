import socket
import time
from concurrent.futures import ThreadPoolExecutor

target = input("Enter target IP or hostname:")

start_port = int(input("Enter starting port: "))
end_port = int(input("Enter ending port: "))

print(f"\nScanning {target} from port {start_port} to {end_port}...\n")

def scan_port(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.5)

    result = sock.connect_ex((target, port))

    if result == 0:
        try:
            service = socket.getservbyport(port, "tcp")
        except OSError:
            service = "Unknown"

        print(f"[+] Port {port} is OPEN → {service}")

    sock.close()

start_time = time.time()

with ThreadPoolExecutor(max_workers=100) as executor:
    executor.map(scan_port, range(start_port, end_port + 1))

end_time = time.time()
scan_time = end_time - start_time

print(f"\nScan complete in {scan_time:.2f} seconds.")