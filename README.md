# disable-ipv6-privacy

A lightweight Python tool that disables IPv6 privacy extensions for NetworkManager profiles to improve IPv6 stability on Linux systems.

Temporary IPv6 privacy addresses (`/128`) can cause routing inconsistencies, broken connectivity, VPN issues, and unpredictable behavior—especially in systems switching between Wi-Fi networks, VPNs, nftables, virtual machines, or bridged interfaces.
This tool enforces stable IPv6 addressing by setting:

```
ipv6.ip6-privacy=0
```

for selected NetworkManager profiles.

---

## **Repository**

GitHub:
[https://github.com/kevinveenbirkenbach/disable-ipv6-privacy](https://github.com/kevinveenbirkenbach/disable-ipv6-privacy)

---

## **Features**

* Disable IPv6 privacy extensions for:

  * **All** NetworkManager connections
  * **Only wired (802-3-ethernet)** connections
* Prevents issues caused by temporary IPv6 privacy addresses:

  * Mixed `/64` and `/128` IPv6 addresses
  * “Destination unreachable” errors
  * Broken IPv6 connectivity over Wi-Fi or Ethernet
  * Unstable routing after switching between iptables and nftables
  * VPN failures (WireGuard / OpenVPN with IPv6)
* Pure Python script with no external dependencies

---

## **Author**

**Kevin Veen-Birkenbach**
[https://veen.world](https://veen.world)

---

## **Usage**

The main script is `main.py`.

### Show help

```bash
python3 main.py --help
```

### Disable IPv6 privacy extensions for **all connections**

```bash
python3 main.py --all
```

This applies:

```
nmcli connection modify "$PROFILE" ipv6.ip6-privacy 0
```

to every NetworkManager profile on the system.

---

### Disable IPv6 privacy extensions **only for wired (802-3-ethernet)** connections

```bash
python3 main.py --wired-only
```

Affects only profiles of type:

```
802-3-ethernet
```

---

## **When to use this tool**

Use this script when:

* your system shows unstable IPv6 connectivity
* you get `Destination unreachable` from your *own* IPv6 address
* NetworkManager assigns both `/64` and `/128` addresses
* using VPNs breaks IPv6 routing
* switching between Wi-Fi networks causes IPv6 failures
* Docker / libvirt / bridges begin misbehaving with IPv6
* nftables or firewall changes caused IPv6 regressions

Typical symptoms that this tool fixes:

* intermittent IPv6 packet loss
* high latency spikes
* `curl -6` failing while IPv4 works
* broken external IPv6 connectivity (Google / Cloudflare etc.)

---

## **Installation**

Clone the repository:

```bash
git clone https://github.com/kevinveenbirkenbach/disable-ipv6-privacy
cd disable-ipv6-privacy
```

Run the tool:

```bash
python3 main.py --all
```

Make the script executable (optional):

```bash
chmod +x main.py
./main.py --wired-only
```

---

## **Reference**

This tool was developed with assistance from ChatGPT.
Conversation reference (ChatGPT, November 2025):
[“Discussion on IPv6 stability issues, NetworkManager, nftables, and privacy extensions.”](https://chatgpt.com/share/6924329b-217c-800f-9171-434e514de029)
