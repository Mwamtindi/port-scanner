import socket

target = input("Enter target IP or hostname:")

start_port = int(input("Enter starting port: "))
end_port = int(input("Enter ending port: "))

print(f"\nScanning {target} from port {start_port} to {end_port}...\n")

for port in range(start_port, end_port + 1):
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

print("\nScan complete.")