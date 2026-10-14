# 🛡️ TheCeltic: Multi-Purpose Cybersecurity Suite

> A comprehensive Python-based cybersecurity toolkit for OSINT, network analysis, credential auditing, and security education.

**TheCeltic** is a command-line interface (CLI) tool that aggregates multiple security features into a single, cohesive environment. It is designed for security professionals, students, and enthusiasts to analyze networks, audit services, and understand attack vectors in a controlled laboratory environment.

## 🌟 Features

The tool includes 10 specialized modules accessible via a main menu:

1.  **🌐 Site Analyzer:** DNS resolution, subdomain enumeration (crt.sh), TLS certificate validation, HTTP header security audit (CSP, HSTS, Cookies), and exposed file detection.
2.  **🔠 Password Generator:** Cryptographically secure password generation using the `secrets` module.
3.  **🗣️ Phone OSINT:** International phone number validation, carrier lookup, and region identification using `phonenumbers`.
4.  **🌎 IP Geolocation:** Multi-source IP geolocation (ipwho.is, ip-api.com) with ISP and organization details.
5.  **🐟 Phisher Engine:** A Zphisher-style phishing simulation tool. Supports local hosting, Cloudflare tunnels, and credential capture for 35+ platforms.
6.  **🦠 Malware Total:** Generates obfuscated payloads (XOR/Base64/PowerShell), identifies IOCs in scripts, and creates persistence mechanisms for Windows/Linux.
7.  **📡 Internet Options:** Wi-Fi auditing assistant (Monitor mode, Handshake analysis, Evil Twin configuration, WPS/WEP auditing).
8.  **📝 Cybersecurity Manual:** An integrated educational guide covering the CIA triad, network protocols, Python for security, and defensive hardening.
9.  **🔑 Brute Force Engine:** Production-grade parallel brute force for SSH, FTP, SMB, and Universal HTTP forms with smart fingerprinting and proxy support.
10. **🕵️ OSINT Aggregator:** Multi-source data collection for IPs, Domains, Emails, and Documents (CPF/CNPJ validation), formatted for Telegram reporting.

## 📋 Requirements

- **Python:** 3.8+
- **OS:** Linux (Kali/Parrot recommended for full functionality), Windows, or macOS
- **Dependencies:**
  - `requests`
  - `phonenumbers`
  - `paramiko` (for SSH brute force)
  - `smbprotocol` (for SMB brute force)
  - `cloudflared` (optional, for public phishing tunnels)

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Emanuel170923/TheCeltic.git
cd TheCelticOrder
python3 TheCelticOrder.py
