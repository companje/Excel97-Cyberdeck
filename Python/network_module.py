import socket,json

def send_udp_message(message, ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    print(message)

    try:
        print(json.dumps(json.loads(message),indent=2))
        try:
            sock.sendto(message.encode(), (ip, port))
            # print(f"Bericht verstuurd naar {ip}:{port}")
        except Exception as e:
            print(f"Fout bij het versturen van het bericht: {e}")
        finally:
            sock.close()

    except Exception as e:
        print(e)