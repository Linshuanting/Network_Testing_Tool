import time
import logging
from scapy.all import IP, ICMP, srl

logger = logging.getLogger(__name__)

class MYICMP:
    def __init__():
        pass

    def ping(self, target, timeout=1):
        pkt = IP(dst=target)/ICMP()
        reply = srl(pkt, timeout=timeout, verbose=0)
        if reply:
            rtt = (reply.time - pkt.sent_time) * 1000
            logger.info(f"  Get Reply from {target}, time:{rtt}, ttl:{reply.ttl}")
            return rtt
        logger.info(f"  Doesn't get Reply from {target}")
        return None
    
    def ping_multiple(self, target, count=4, interval=1, timeout=1, retry=3):
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
                    time.sleep(0.2)
            
            if not success:
                logger.info(f"  Lost Packet from {target}")
                lost += 1
            
            time.sleep(interval)
        
        total_send = count
        total_received = len(rtt_samples)
        packet_loss = round((1 - total_received/total_send) * 100, 2)
        rtt_avg = round(sum(rtt_samples) / total_received, 2) if rtt_samples else None
        rtt_max = max(rtt_samples) if rtt_samples else None
        rtt_min = min(rtt_samples) if rtt_samples else None
        
        return {
            "RTT_samples": rtt_samples,
            "RTT_avg": f"{rtt_avg}ms" if rtt_avg else "N/A",
            "RTT_max": rf"{rtt_max}ms" if rtt_max else "N/A",
            "RTT_min": f"{rtt_min}ms" if rtt_min else "N/A",
            "packet_loss": f"{packet_loss}%"
        }