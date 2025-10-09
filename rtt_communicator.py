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
                # Since the data is cobs encoded, we can read till 0x00
                data = bytearray()
                while True:
                    byte = s.recv(1)
                    if not byte:
                        print("Connection closed by the server.")
                        return
                    if byte == b'\x00':
                        break
                    data.extend(byte)
                if data:
                    print(f"{data} {len(data)}")  # Here you can decode the COBS data if needed

        except ConnectionRefusedError:
            print(f"Error: Connection refused. Is OpenOCD running and is the RTT server enabled on port {PORT}?")
        except Exception as e:
            print(f"An error occurred: {e}")

def main():
    read_from_socket()
    return 0
    
if __name__ == "__main__":
    sys.exit(main())
