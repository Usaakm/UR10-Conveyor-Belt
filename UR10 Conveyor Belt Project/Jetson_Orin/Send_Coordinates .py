import socket
import time

HOST = "192.168.0.2" # The remote host
PORT = 30002 # The same port as used by the server

print("Starting Program")


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
time.sleep(0.5)

# print("Set output 1 and 2 high")

# s.send("set_digital_out(1,True)\n".encode())
# time.sleep(0.1)

# s.send("set_digital_out(2,False)" + "\n")
# time.sleep(2)

print("Robot starts Moving to 3 positions based on joint positions")

s.send("movej(p[-0.06, -0.72, 0.03, 3.1, 0, 0], a=0.5, v=0.25)\n".encode())
time.sleep(10)



# print("Set output 1 and 2 low")

# s.send("set_digital_out(1,False)" + "\n")
# time.sleep(0.1)

# s.send("set_digital_out(2,False)" + "\n")
# time.sleep(0.1)

# count = count + 1
# print("The count is:", count)

# print("Program finish")

# time.sleep(1)
# data = s.recv(1024)

# s.close()
# print("Received", repr(data))

# print("Status data received from robot")
