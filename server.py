import socket
import geopy.distance

# Thiết lập kết nối socket
server_address = ('192.168.0.107', 10000)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(server_address)

# Đợi kết nối từ client
sock.listen(2)
print(f"Đang chờ kết nối từ DroneClient...")

# Khởi tạo đối tượng lưu trữ tọa độ của drone 1 và drone 2.
drone1_coord = None
drone2_coord = None

# Hàm xử lý khi có dữ liệu GPS từ client
def handle_gps_coords(data):
    global drone1_coord, drone2_coord
    try:
        drone_info = data.decode().split(',')
        drone_name = drone_info[0]
        lat = float(drone_info[1])
        lon = float(drone_info[2])
        alt = float(drone_info[3])
        
        # Cập nhật tọa độ của Drone tương ứng (dựa vào tên Drone)
        if drone_name == 'drone1':
            drone1_coord = (lat, lon, alt)
        elif drone_name == 'drone2':
            drone2_coord = (lat, lon, alt)
        else:
            print(f"Tên Drone không hợp lệ: {drone_name}")
            return
            
        print(f"Đã nhận tọa độ GPS của {drone_name}: {lat}, {lon}, {alt}")
        
        # Tính toán khoảng cách giữa 2 Drone (nếu cả 2 đều đã gửi tọa độ lên)
        if drone1_coord and drone2_coord:
            distance = geopy.distance.distance(drone1_coord[:2], drone2_coord[:2]).meters
            print(f"Khoảng cách giữa Drone 1 và Drone 2: {distance} mét.")
            
    except Exception as e:
        print(f"Lỗi khi xử lý dữ liệu từ client: {e}")

# Chạy vòng lặp để nhận dữ liệu từ DroneClient
while True:
    # Chấp nhận kết nối
    client_connection, client_address = sock.accept()
    try:
        # Nhận dữ liệu từ DroneClient
        data = client_connection.recv(1024)
        while data:
            # Xử lý tọa độ GPS
            handle_gps_coords(data)
            # Tiếp tục chờ dữ liệu từ DroneClient
            data = client_connection.recv(1024)
    except Exception as e:
        print(f"Lỗi khi nhận dữ liệu từ DroneClient: {e}")
    finally:
        # Đóng kết nối
        client_connection.close()
