import sys
import socket


def main():
    if len(sys.argv != 3):
        print("Usage: python3 server.py <server_ip> <server_port>")
        sys.exit(1)
