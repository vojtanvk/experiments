#!/usr/bin/env python3

import sys
import argparse
import socket

sys.path.append("build/")

import RTTMetricsDeserializer as des
import rtt_plotter as plotter
import pandas as pd
import numpy as np

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
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s, open("socket_ouput.bin", "wb") as f:
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
                    des.deserialize(data)
                    timestamp = des.get_timestamp()
                    res = des.read_raw_acceleration()
                    print(des.get_type(), timestamp, res.x, res.y, res.z)
                    f.write(data + b'\0')  # Write the received data to file with delimiter
                    
        except ConnectionRefusedError:
            print(f"Error: Connection refused. Is OpenOCD running and is the RTT server enabled on port {PORT}?")
        except Exception as e:
            print(f"An error occurred: {e}")

def read_form_file(filepath: str):
    timestamps = []
    x_values = [] 
    y_values = []
    z_values = []
    with open(filepath, "rb") as f:
        try:
            while True:
                packet = bytearray()
                b = f.read(1)
    
                if not b:
                    break
    
                # read whole packet            
                while(b != b'\0'):
                    packet.extend(b)
                    b = f.read(1)
                des.deserialize(packet)
                timestamp = des.get_timestamp()
                timestamps.append(timestamp)
                
                res = des.read_raw_acceleration()
                
                print(des.get_type(), timestamp, res.x, res.y, res.z)
                x_values.append(res.x)
                y_values.append(res.y)
                z_values.append(res.z)
                # print(res.x)  
            
        except Exception as e:
            print(f"An error occured: {e}")

    datafr = pd.DataFrame({
        "Type": "RawAcceleration",
        "Timestamp": timestamps,
        "X": x_values,
        "Y": y_values,
        "Z": z_values
    })
    
    plotter.plot_sensor_data(datafr)


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
