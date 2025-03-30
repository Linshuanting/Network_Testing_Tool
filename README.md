# Network_Testing_Tool

A parallelized ICMP ping testing tool built with Python and Scapy. It supports both IPv4 and IPv6, and provides detailed logging and metrics like RTT (Round Trip Time), packet loss, and more.

---

##  Features
- ✅ Support for both **IPv4** and **IPv6**
- ✅ Collects detailed **RTT statistics** and packet loss
- ✅ Built-in **multi-threaded** ping execution
- ✅ Automatic **ICMP echo retry** with configurable parameters
- ✅ Logs output to **both console and file** (with timestamped entries)

---

##  Environment
- Ubuntu 22.04
- Python 3.10.2

---

##  Requirements
```bash
pip install scapy
```

---

##  Project Structure
```
network_testing_tool/
├── icmp.py               # Core ICMP ping logic (parallel, IPv4+IPv6)
├── log.py                # Logger configuration (file + console)
├── network_tool.py       # Main script to execute the test
├── log/                  # Folder where logs are saved
│   └── network_test.log  # Output log file
└── README.md             # Documentation
```

---

##  Usage
```bash
sudo python3 network_tool.py \
  --targets 8.8.8.8 192.168.1.1 fd00::1 \
  --duration 2 \
  --rate 2 \
  --retry-count 2 \
  --retry-interval 0.5
```

### Parameters
| Argument           | Description                                 | Default |
|--------------------|---------------------------------------------|---------|
| `--targets`        | List of IP addresses to ping                | Required |
| `--duration`       | Duration in seconds                        | `2`     |
| `--rate`           | Pings per second                           | `2`     |
| `--retry-count`    | Retry if no reply                          | Optional |
| `--retry-interval` | Interval between retries (in seconds)      | Optional |

---

##  Output Sample (JSON)
```json
{
  "start_time": "2025-03-28 15:21:42",
  "end_time": "2025-03-28 15:21:44",
  "rate": "2 packets/sec",
  "results": {
    "8.8.8.8": {
      "RTT_samples": [112, 127, 121],
      "RTT_avg": "120.0ms",
      "RTT_max": "127ms",
      "RTT_min": "112ms",
      "packet_loss": "0.0%"
    }
  }
}
```

> 📁 Log files are saved automatically in `./log/network_test.log`


