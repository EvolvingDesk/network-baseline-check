#!/usr/bin/env python3
import argparse
import socket
import sys
from datetime import datetime, timezone

DEFAULT_PORTS = [22, 80, 443, 3389]

def try_connect(host: str, port: int, timeout: float) -> bool:
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except Exception:
        return False

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Starter template for basic network checks. Not production ready."
    )
    parser.add_argument("host", help="Target host or IP")
    parser.add_argument("--ports", default=",".join(str(p) for p in DEFAULT_PORTS), help="Comma separated ports")
    parser.add_argument("--timeout", type=float, default=0.5, help="Connect timeout seconds")
    args = parser.parse_args()

    ports = []
    for part in args.ports.split(","):
        part = part.strip()
        if not part:
            continue
        try:
            ports.append(int(part))
        except ValueError:
            print(f"Invalid port value: {part}")
            return 2

    now = datetime.now(timezone.utc).isoformat()
    print(f"Tool: network-audit-template")
    print(f"Generated: {now}")
    print(f"Target: {args.host}")
    print("")
    print("Port checks:")
    open_count = 0
    for p in ports:
        is_open = try_connect(args.host, p, args.timeout)
        status = "OPEN" if is_open else "closed"
        print(f"  {args.host}:{p} {status}")
        if is_open:
            open_count += 1

    print("")
    print(f"Summary: open {open_count} , checked {len(ports)}")
    print("Exit code: 0")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
