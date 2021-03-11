import argparse
import subprocess
import os

path = os.path.dirname(os.path.realpath(__file__)) + '/'


def run_server(port):
    subprocess.run( ['java', '-jar', 
        path + 'marioai-server-0.1-jar-with-dependencies.jar',
        '-p', str(port)])


def run_server_in_background(port):
    print('running the server in the background')
    
    server_process = subprocess.Popen(
        ['java', '-jar', path + 'marioai-server-0.1-jar-with-dependencies.jar',
            '-p', str(port)])

    return server_process


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-p', '--port', type=int, default=8080, 
            help='specify the server port.')
    parser.add_argument('-b', '--background', action='store_true',
            help='specify whether to run the server as background process')
    args = parser.parse_args()

    if args.background:
        server_process = run_server_in_background(args.port)
    else:
        run_server(args.port)


if __name__ == '__main__':
    main()
