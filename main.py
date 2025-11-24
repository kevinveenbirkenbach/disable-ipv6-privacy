#!/usr/bin/env python3
import argparse
import subprocess
import sys


def run(cmd):
    """Run a shell command and return output lines."""
    try:
        out = subprocess.check_output(cmd, shell=True, text=True)
        return out.strip().splitlines()
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {cmd}")
        print(e.output)
        sys.exit(1)


def disable_privacy_for_all():
    """Disable IPv6 privacy extensions for all NetworkManager connections."""
    connections = run("nmcli -t -f NAME connection show")
    print("Disabling IPv6 privacy for ALL connections:")

    for name in connections:
        print(f" → {name}")
        subprocess.call(f"sudo nmcli connection modify '{name}' ipv6.ip6-privacy 0", shell=True)


def disable_privacy_for_wired():
    """Disable IPv6 privacy extensions only for wired (802-3-ethernet) connections."""
    lines = run("nmcli -t -f NAME,TYPE connection show")
    print("Disabling IPv6 privacy for wired (802-3-ethernet) connections:")

    for line in lines:
        name, ctype = line.split(":", 1)
        if ctype == "802-3-ethernet":
            print(f" → {name}")
            subprocess.call(f"sudo nmcli connection modify '{name}' ipv6.ip6-privacy 0", shell=True)


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Disable IPv6 privacy extensions (temporary IPv6 addresses) for NetworkManager profiles.\n\n"
            "This tool is useful when Linux clients experience unstable IPv6 behaviour, such as:\n"
            " - intermittent 'Destination unreachable' errors\n"
            " - mixed /64 and /128 IPv6 addresses\n"
            " - unstable connectivity in VPN/Wi-Fi environments\n"
            " - routing problems caused by temporary IPv6 privacy addresses\n\n"
            "When to use it:\n"
            " - after switching between iptables and nftables\n"
            " - when IPv6 becomes unstable in complex networking setups\n"
            " - if your system uses multiple networks, VPNs, or roaming Wi-Fi\n"
            " - when NetworkManager creates unwanted temporary IPv6 addresses\n\n"
            "The script can disable privacy extensions for ALL connections or ONLY for wired profiles."
        ),
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument(
        "--wired-only",
        action="store_true",
        help="Disable IPv6 privacy extensions only for wired (802-3-ethernet) connections."
    )

    parser.add_argument(
        "--all",
        action="store_true",
        help="Disable IPv6 privacy extensions for ALL NetworkManager connections."
    )

    args = parser.parse_args()

    if args.wired_only:
        disable_privacy_for_wired()
    elif args.all:
        disable_privacy_for_all()
    else:
        print("No mode selected. Use --wired-only or --all.")
        sys.exit(1)


if __name__ == "__main__":
    main()
