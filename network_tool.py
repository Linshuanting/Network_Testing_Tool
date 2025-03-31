import argparse
import time
import json
from scapy.all import *
from icmp import MYICMP
from log import logger

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--targets", nargs="+", required=True)
    parser.add_argument("--duration", type=int, default=2)
    parser.add_argument("--rate", type=int, default=2)
    parser.add_argument("--retry-count", type=int)
    parser.add_argument("--retry-interval", type=float)
    parser.add_argument("--parallel", action="store_true")
    args = parser.parse_args()

    count = args.duration * args.rate
    interval = 1/args.rate

    start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    
    icmp_kwargs = {
        "targets": args.targets,
        "timeout": 1,
        "count": count,
        "interval": interval
    }
    if args.retry_count is not None:
        icmp_kwargs["retry"] = args.retry_count
    if args.retry_interval is not None:
        icmp_kwargs["retry_interval"] = args.retry_interval

    myicmp = MYICMP()
    
    if args.parallel:
        results = myicmp.ping_targets_multithread(**icmp_kwargs)
    else:
        results = myicmp.ping_targets(**icmp_kwargs)

    end_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    output = {
        "start_time": start_time,
        "end_time": end_time,
        "rate": f"{args.rate} packets/sec",
        "results": results
    }

    print(json.dumps(output, indent=4))




