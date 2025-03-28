import argparse
import time
import json
import logging
import os, sys
from scapy.all import *
from icmp import MYICMP
from log import logger

def icmp(targets, timeout=1, count=None, interval=None, retry=None, retry_interval=None):
    icmp = MYICMP()

    results = {}

    for target in targets:
        kwargs = {
            "target": target,
            "timeout": timeout
        }

        if count is not None:
            kwargs["count"] = count
        if interval is not None:
            kwargs["interval"] = interval
        if retry is not None:
            kwargs["retry"] = retry
        if retry_interval is not None:
            kwargs["retry_interval"] = retry_interval

        logger.info(f"--- Start Ping Target:{target} ---")

        res = icmp.ping_multiple(**kwargs)
        results[target] = res
    
    return results

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--targets", nargs="+", required=True)
    parser.add_argument("--duration", type=int, default=2)
    parser.add_argument("--rate", type=int, default=2)
    parser.add_argument("--retry-count", type=int)
    parser.add_argument("--retry-interval", type=float)
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

    results = icmp(**icmp_kwargs)

    end_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    output = {
        "start_time": start_time,
        "end_time": end_time,
        "rate": f"{args.rate} packets/sec",
        "results": results
    }

    print(json.dumps(output, indent=4))




