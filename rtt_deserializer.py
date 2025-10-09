#!/usr/bin/env python3

import sys
import argparse
import socket

sys.path.append("build/")

import RTTMetricsDeserializer as des

HOST = 'localhost'
PORT = 60002

def arguments():
    parser = argparse.ArgumentParser(
        prog='RTT Communicator',
        description='Script to read data from RTT. Can be run with a file in the stead of RTT connection. In both cases it is expected binary COBS encoded data in the format: TYPE | TIMESTAMP | DATA and the recorded DATA must be defined within the "rtt_metrics" module located in the "deserialization" directory'
        
    )
    
    parser.add_argument('-f', '--file', type=str, required=False, help='option to read from file instead of RTT')
    
    
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

def read_form_file(filepath: str):
    with open(filepath, "rb") as f:
        try:
            while(True):
                # TODO this needs extensive rework to be usable in the future
                # For now it works only with accelerometer data (1 byte COBS OVERHEAD | 1 byte TYPE | 4 bytes TIMESTAMP | 6 bytes DATA)
                packet = bytearray(f.read(12))
                # print(packet)
                des.deserialize(packet)
                print(des.get_type())
                print(des.get_timestamp())
                res = des.read_raw_acceleration()
                print(res.x)
                
                
            
            
        except Exception as e:
            print(f"An error occured: {e}")

def deserialize_packet(packet: bytearray):
    ...

def main():
    
    args = arguments()
    
    print(args.file)
    
    if(args.file) :
        read_form_file(args.file)
    else:
        read_from_socket()
    return 0
    
if __name__ == "__main__":
    sys.exit(main())
