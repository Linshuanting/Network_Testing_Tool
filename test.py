import subprocess
import platform
import time
import logging
from scapy.all import IP, ICMP, sr1, conf

def detect_interface_mode():
    try:
        result = subprocess.check_output("ip route", shell=True).decode()
        if "eth0" in result or "ens" in result:
            return "Likely Bridge or NAT (check DHCP route)"
        elif "enp0s" in result:
            return "Likely Bridge"
        elif "default via" in result:
            return "Default gateway present"
        else:
            return "Unknown network mode"
    except Exception as e:
        return f"Error detecting interface: {e}"

def try_ping(target="127.0.0.1"):
    logging.info(f"Trying Scapy ping to {target}")
    conf.use_pcap = True  # 强制使用 pcap 抓包（更穩定）

    pkt = IP(dst=target) / ICMP()
    start = time.time()
    reply = sr1(pkt, timeout=2, verbose=0)
    end = time.time()

    if reply:
        rtt = (end - start) * 1000
        logging.info(f"✅ Reply from {target}: RTT={rtt:.2f}ms, TTL={reply.ttl}")
        return True
    else:
        logging.warning(f"❌ No reply from {target}. May be blocked, filtered or dropped.")
        return False

def main():
    logging.basicConfig(
        level=logging.INFO,
        format='[%(asctime)s] %(levelname)s: %(message)s',
        datefmt='%H:%M:%S'
    )

    logging.info("--- Running Scapy Ping Environment Diagnostic ---")
    mode = detect_interface_mode()
    logging.info(f"🔍 Detected Network Mode: {mode}")

    for ip in ["127.0.0.1", "8.8.8.8", "1.1.1.1"]:
        try_ping(ip)

    logging.info("--- Diagnosis Complete ---")

if __name__ == "__main__":
    main()
