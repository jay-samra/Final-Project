import sys
import socket


def main():
    if len(sys.argv != 2):
        print("Usage: python3 server.py <server_port>")
        sys.exit(1)
