from datetime import datetime
import time
import serial
import serial.tools.list_ports
import logging
import argparse
import sys

ERROR_INVALID_PORT = "ERROR: Invalid port ... exiting"

def handle_args():
  parser = argparse.ArgumentParser()

  parser.add_argument("-l", "--list",action='store', help="List available serial ports and exit", dest='list', default=None, nargs='?')
  required_args = parser.add_argument_group("required named arguments")
  
  # Required named arguments
  required_args.add_argument("-p", "--port", help="Serial port")
  required_args.add_argument("-b", "--baud", help="Baud rate")

  args = parser.parse_args()

  return args

def list_serial_ports():
  ports = serial.tools.list_ports.comports()
  return ports

def main() -> None:
  serial_config = {
    "port": None,
    "baud_rate": 9600,
    "timeout": 5
  }

  log_file_name = f"serial-logger-{datetime.now().strftime('%Y-%m-%d')}.log"
  logging.basicConfig(filename=log_file_name, encoding='utf-8', level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S %z')

  print("Python Serial Logger")
  print("Logging to " + log_file_name)

  args = handle_args()

  if '-l' in sys.argv:
    serial_ports = list_serial_ports()
    for port, desc, hwid in sorted(serial_ports):
      print(f"{port}: {desc} {hwid}")
    sys.exit(0)
  
  if args.port:
    serial_config["port"] = args.port
  else:
    print(ERROR_INVALID_PORT)
    sys.exit(1)

  if args.baud:
    serial_config["baud_rate"] = args.baud
  else:
    print("ERROR: Baud rate required")
    sys.exit(1)

  serial_ports = list_serial_ports()
  is_serial_port_available = False
  
  for port, desc, hwid in sorted(serial_ports):
    print(f"{port}: {desc} {hwid}")
    if port == serial_config["port"]:
      is_serial_port_available = True
  
  if is_serial_port_available == False:
    print(ERROR_INVALID_PORT)
    sys.exit(1)

  with serial.Serial(serial_config["port"], serial_config["baud_rate"], timeout=serial_config["timeout"]) as ser:
    while True:
      line = ser.readline()
      logging.info(line.decode('utf-8'))
      print(line.decode('utf-8'))
      time.sleep(1)



if __name__ == '__main__':
  main()