import sys
import signal
from random import randint
from compiler import Compiler
from cpu import CPU

def inject (sig, frame):
    where = input('\n> Inject fault? (r = fault register, s = skip instruction, q = quit) ')
    if where == 'q':
        sys.exit(1)
    elif where == 's':
        skip = int(input('> How many instruction to skip? '))
        cpu._ip += skip
        print('! ' + str(skip) + ' instructions skipped')
    elif where == 'r':
        reg = int(input('> Which register? (0-'+str(cpu._reg._size)+') '))
        what = input('> Zero or random? (z = zero, r = random) ')
        if what == 'z':
            cpu._reg._mem[reg] = 0
            print('! r' + str(reg) + ' zeroized')
        elif what == 'r':
            cpu._reg._mem[reg] = randint(0, cpu._ram._size)
            print('! r' + str(reg) + ' randomized')
    print('> Resuming…')

if sys.argv[1] == '-i':
    signal.signal(signal.SIGINT, inject)
    sys.argv.pop(1)

program = Compiler().compile(sys.argv[1])

cpu = CPU(1048576, 32, program, sys.argv[2])
cpu.run()
