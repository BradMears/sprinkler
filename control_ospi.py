#!/usr/bin/env python3
'''Testbed for controlling the OpenSprinklerPi from python.'''
import subprocess

NUM_ZONES = 10

HOST = 'ospi'
PORT = 8080

def set_zone(zone, state):
    assert(1 <= zone <= NUM_ZONES)
    assert(state == 0 or state == 1)

    s = subprocess.run(['wget', 
                        f'http://{HOST}:{PORT}/sn{zone}={state}&t=0',
                        '-a', './ospi.log',
                        '-O', '/dev/null'], capture_output=False)

    if s.returncode != 0:
        print('Uh-oh... Something went wrong. Return code = ', s.returncode)
        print(s.args)
        return s.returncode

if __name__ == '__main__':
    import sys
    
    try:
        zone = int(sys.argv[1])
    except BaseException:
        print('Specify the zone number on the cmd line')
        sys.exit(1)

    try:
        state = int(sys.argv[2])
    except BaseException:
        print('Specify 0 (off) or 1 (on) on the cmd line')
        sys.exit(1)

    set_zone(zone, state)
    