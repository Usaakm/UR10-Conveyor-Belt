import socket
import struct
import time

HOST = "192.168.0.2" # The remote host
PORT = 30002 # The same port as used by the server

# print("Starting Program")

# # Modify this value to control how many times the loop will execute
# loop_count = 1

# for count in range(loop_count):
#     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     s.connect((HOST, PORT))
#     time.sleep(0.5)
#     print("Getting encoder data...")
#     cmd = "encoder_get_tick_count()\n"
#     cmd = "movel([-0.7, -0.7, 0.6, 0.3, 0.1, 0], a=1.0, v=0.1)" + "\n"
#     cmd = ()
#     s.send(cmd)
#     #s.send("powerdown()\n".encode())
#     time.sleep(0.1)
#     data = s.recv(4)  # Expecting 4 bytes for an integer
#     encoder_data = struct.unpack("!i", data)[0]  # Unpack as a signed integer
#     print("Encoder data:", encoder_data)
#     s.close()

# print("Program finish")

# # Connect to the robot
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.connect((HOST, PORT))

# # Send a URScript command to shut down the robot
# cmd = "shutdown()\n"
# #s.send(cmd.encode())

# # Close the connection
# s.close()

# Echo client program
# import socket


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

s.send ("set_digital_out(2,False)" + "\n")

data = s.recv(1024)

s.close()

print ("Received", repr(data))




# Echo client program
# import socket

# HOST = "192.168.0.2" # The remote host
# PORT = 30002 # The same port as used by the server

# while True:

#     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     s.connect((HOST, PORT))






#     s.send("hello".encode())

    # data = s.recv(1024).decode('ascii')

    # message_recieved = data

    #print("Received", repr(message_recieved))


# s.close()



# def send_variable_to_pc(variable_name):
#     # Open a socket to your PC
#     import socket
#     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     s.connect(("YOUR_PC_IP_ADDRESS", YOUR_TCP_PORT))

#     # Send the variable value to your PC
#     var_value = eval(variable_name)  # Get the value of the variable by its name
#     s.send(str(var_value).encode())

#     # Close the socket
#     s.close()

# # Example usage: send the value of a variable named "my_var" to your PC
# send_variable_to_pc("my_var")








# import socket

# # create a TCP/IP socket
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# # define the IP address and port number of the robot
# robot_ip = '192.168.0.2'
# robot_port = 5000

# # connect to the robot
# s.connect((robot_ip, robot_port))

# # receive data from the robot
# data = s.recv(1024).decode('utf-8')

# # print the received data
# print(data)

# # close the connection
# s.close()







# import socket

# # create a socket object
# server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# # bind the socket to a specific IP address and port
# # host = "192.168.0.2"  # listen on all available interfaces
# # port = 50000  # choose a port number
# # server_socket.bind((host, port))
# server_socket.bind(("0.0.0.0", 50000)) 

# # listen for incoming connections
# server_socket.listen(1)  # allow up to 1 connection

# while True:
#     # accept incoming connections
#     client_socket, client_address = server_socket.accept()

#     # receive data from the client
#     data = client_socket.recv(1024)  # receive up to 1024 bytes of data

#     # process the data
#     if data:
#         # send a response back to the client
#         response = 'Thank you for connecting'
#         client_socket.send(response.encode())

#     # close the client socket
#     client_socket.close()

# # close the server socket
# siserver_socket.close()


# import socket

# def server_program():
#     # get the hostname
#     host = ""
#     port = 50000  # initiate port no above 1024

#     server_socket = socket.socket()  # get instance
#     # look closely. The bind() function takes tuple as argument
#     server_socket.bind((host, port))  # bind host address and port together

#     # configure how many client the server can listen simultaneously
#     server_socket.listen(1)
#     conn, address = server_socket.accept()  # accept new connection
#     #print("Connection from: " + str(address))

#     while True:
#         # receive data stream. it won't accept data packet greater than 1024 bytes
#         data = conn.recv(1024).decode()
#         if not data:
#             # if data is not received break
#             break
#         print(str(data))
#         # data = input(' -> ')
#         # conn.send(data.encode())  # send data to the client

#     conn.close()  # close the connection


# if __name__ == '__main__':
#     server_program()


# import socket

# def server_program():
#     # get the hostname
#     host = "192.168.0.2"
#     port = 50000  # initiate port no above 1024

#     server_socket = socket.socket()  # get instance
#     # look closely. The bind() function takes tuple as argument
#     server_socket.bind((host, port))  # bind host address and port together

#     # configure how many client the server can listen simultaneously
#     server_socket.listen(1)
#     conn, address = server_socket.accept()  # accept new connection
#     #print("Connection from: " + str(address))

#     conn.send("movel([-0.7, -0.7, 0.6, 0.3, 0.1, 0], a=1.0, v=0.1)" + "\n")
#     # while True:
#     #     # receive data stream. it won't accept data packet greater than 1024 bytes
#     #     data = conn.recv(1024).decode()
#     #     print(str(data))
#     #     conn.send("movel([-0.7, -0.7, 0.6, 0.3, 0.1, 0], a=1.0, v=0.1)" + "\n")

