import sys
import argparse
import socket

HOST = 'localhost'
PORT = 60002

def arguments():
    parser = argparse.ArgumentParser(
        prog='Program name',
        description='Description'
    )
    
    parser.add_argument('--option')
    
    
    return parser.parse_args()

def read_from_socket():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            # Connect the socket to the server's address
            s.connect((HOST, PORT))
            print(f"Connected to OpenOCD RTT server at {HOST}:{PORT}")

            # Read data in a loop
            while True:
                # Receive data in chunks of 1024 bytes
                data = s.recv(1024)
                if not data:
                    # If no data is received, the connection is closed
                    print("Connection closed by peer.")
                    break
                # Decode the received bytes and print to console
                print(data, end='')

        except ConnectionRefusedError:
            print(f"Error: Connection refused. Is OpenOCD running and is the RTT server enabled on port {PORT}?")
        except Exception as e:
            print(f"An error occurred: {e}")

def main():
    read_from_socket()
    return 0
    
if __name__ == "__main__":
    sys.exit(main())