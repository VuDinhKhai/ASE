import socket
import threading
import geopy.distance

HOST = '192.168.0.107'
PORT = 8888

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen()

# Khởi tạo vị trí ban đầu của 2 drone
position_drone_1 = (0,0,0)
position_drone_2 = (0,0,0)
msg = f"Position of drone_1 is {position_drone_1}\nPosition of drone_2 is {position_drone_2}"


def handle_connection(conn, addr, drone_id):
    print(f"New connection from {addr}")
    global position_drone_1, position_drone_2, msg
    
    conn.sendall(msg.encode('utf-8'))
    
    while True:
        data = conn.recv(1024)
        if not data:
            break

        lat, lon, alt = [float(x) for x in data.decode('utf-8').split(',')]
        
        if drone_id == 1:
            position_drone_1 = (lat, lon, alt)
        elif drone_id == 2:
            position_drone_2 = (lat, lon, alt)
        
        distance = geopy.distance.distance(position_drone_1[:2], position_drone_2[:2]).meters
        new_msg = f"Position of drone_{drone_id +1 } is {position_drone_1 if drone_id == 1 else position_drone_2}\nDistance between drone_1 and drone_2 is {distance} meters."
        
        # Gửi chuỗi string thông báo mới cho client
        conn.sendall(new_msg.encode('utf-8'))
    conn.close()

while True:
    conn, addr = s.accept()
    
    # Tạo thread
    if threading.active_count() < 3:
        drone_id = threading.active_count() - 1
        t = threading.Thread(target=handle_connection, args=(conn, addr, drone_id))
        t.start()
    else:
        error_msg = "Server is busy. Please try again later."
        conn.sendall(error_msg.encode('utf-8'))
        conn.close()
