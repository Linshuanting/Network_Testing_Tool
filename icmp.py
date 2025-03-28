import time
import ipaddress
from scapy.all import IP, ICMP, IPv6, ICMPv6EchoRequest, sr1, sniff, conf
from log import logger
from concurrent.futures import ThreadPoolExecutor, as_completed

conf.use_pcap = True

class MYICMP:
    def __init__(self):
        pass

    def ping(self, target, timeout=1):
        try:
            ip_ver = ipaddress.ip_address(target).version
            if ip_ver == 6:
                pkt = IPv6(dst=target)/ICMPv6EchoRequest()
            else:
                pkt = IP(dst=target)/ICMP()
        except ValueError:
            logger.error(f"Invalid IP address: {target}")
            return None

        start = time.time()
        reply = sr1(pkt, timeout=timeout, verbose=0)

        if reply:
            rtt = round((reply.time - start) * 1000, 0)
            logger.info(f"  Get Reply from {target}, time:{rtt}ms, ttl:{reply.ttl if hasattr(reply, 'ttl') else 'N/A'}")
            return rtt
        logger.info(f"  Doesn't get Reply from {target}")
        return None

    
    def ping_multiple(self, target, count=4, interval=1, timeout=1, retry=3, retry_interval=0.2):
        rtt_samples = []
        lost = 0

        for i in range(count):
            success = False
            for j in range(retry+1):
                if j == 0:
                    logger.info(f"Ping {target} with timeout:{timeout}")
                else:
                    logger.info(f"  Retry connect {target}")

                rtt = self.ping(target, timeout=timeout)
                if rtt is not None:
                    rtt_samples.append(rtt)
                    success = True
                    break
                else:
                    time.sleep(retry_interval)
            
            if not success:
                logger.info(f"  Lost Packet from {target}")
                lost += 1
            
            time.sleep(interval)
        
        total_send = count
        total_received = len(rtt_samples)
        packet_loss = round((1 - total_received/total_send) * 100, 2)
        rtt_avg = round(sum(rtt_samples) / total_received, 2) if rtt_samples else None
        rtt_max = round(max(rtt_samples), 2) if rtt_samples else None
        rtt_min = round(min(rtt_samples), 2) if rtt_samples else None
        
        return {
            "RTT_samples": rtt_samples,
            "RTT_avg": f"{rtt_avg}ms" if rtt_avg else "N/A",
            "RTT_max": rf"{rtt_max}ms" if rtt_max else "N/A",
            "RTT_min": f"{rtt_min}ms" if rtt_min else "N/A",
            "packet_loss": f"{packet_loss}%"
        }
    
    def ping_targets(self, targets, timeout=1, count=None, interval=None, retry=None, retry_interval=None):
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
        
    def ping_targets_multithread(self, targets, timeout=1, count=None, interval=None, retry=None, retry_interval=None):
        results = {}

        def ping_task(target):
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
            return target, self.ping_multiple(**kwargs)

        with ThreadPoolExecutor(thread_name_prefix=f"ICMP") as executor:
            futures = [executor.submit(ping_task, target) for target in targets]
            for future in as_completed(futures):
                target, result = future.result()
                results[target] = result

        return results
    
