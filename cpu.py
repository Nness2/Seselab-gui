import sys
from memory import Memory
from probe  import Probe
from exn    import *

class CPU:

    def __init__ (self, ram_size, reg_count, code, consolog):
        self._ram = Memory(ram_size)
        self._reg = Memory(reg_count)
        self.__ra = reg_count - 1
        self.__sp = reg_count - 2
        self._code = code
        self._probe = Probe(consolog)

    def value (self, val):
        if val[0] == 'imm':
            return val[1]
        if val[0] == 'reg':
            return self._reg[val[1]]
        if val[0] == 'mem':
            return self._ram[val[1]]
        if val[0] == 'ref':
            v = self.value(val[1])
            if len(val) == 3:
                v += self.value(val[2])
            return self._ram[v]

    def write (self, addr, val):
        if addr[0] == 'imm':
            raise WriteError
        if addr[0] == 'reg':
            self._reg[addr[1]] = val
        if addr[0] == 'mem':
            self._ram[addr[1]] = val
        if addr[0] == 'ref':
            a = self.value(addr[1])
            if len(addr) == 3:
                a += self.value(addr[2])
            self._ram[a] = val

    def cycle (self, ip):
        instr = self._code[ip][0]
        opcode = instr[0]

        # opcodes with no arguments
        if opcode == 'nop':
            pass
        elif opcode == 'ret':
            return self.value(('reg', self.__ra))
        else:
            # opcode with 1 argument
            dst = instr[1]
            if opcode == 'cal':
                self.write(('reg', self.__ra), ip + 1)
                return self.value(dst)
            if opcode == 'jmp':
                return self.value(dst)
            if opcode == 'dbg':
                self._probe.dbg(dst)
            elif opcode == 'prn':
                print(self.value(dst), end='')
            elif opcode == 'prx':
                print(format(self.value(dst), '02x'), end='')
            elif opcode == 'prX':
                print(format(self.value(dst), '04x'), end='')
            elif opcode == 'prc':
                print(chr(self.value(dst)), end='')
            else:
                # opcodes with 2 arguments
                val1 = instr[2]
                if opcode == 'prs':
                    ptr = self.value(dst)
                    for i in range(0, self.value(val1)):
                        print(chr(self._ram[ptr+i]), end='')
                    print('')
                elif opcode == 'mov':
                    self.write(dst, self.value(val1))
                elif opcode == 'not':
                    self.write(dst, 0xffff ^ self.value(val1))
                else:
                    # opcodes with 3 arguments
                    val2 = instr[3]
                    if opcode == 'beq':
                        if self.value(val1) == self.value(val2):
                            return self.value(dst)
                    elif opcode == 'bne':
                        if self.value(val1) != self.value(val2):
                            return self.value(dst)
                    elif opcode == 'and':
                        self.write(dst, self.value(val1) & self.value(val2))
                    elif opcode == 'orr':
                        self.write(dst, self.value(val1) | self.value(val2))
                    elif opcode == 'xor':
                        self.write(dst, self.value(val1) ^ self.value(val2))
                    elif opcode == 'lsl':
                        self.write(dst, self.value(val1) << self.value(val2))
                    elif opcode == 'lsr':
                        self.write(dst, self.value(val1) >> self.value(val2))
                    elif opcode == 'min':
                        self.write(dst, min(self.value(val1), self.value(val2)))
                    elif opcode == 'max':
                        self.write(dst, max(self.value(val1), self.value(val2)))
                    elif opcode == 'add':
                        self.write(dst, self.value(val1) + self.value(val2))
                    elif opcode == 'sub':
                        self.write(dst, self.value(val1) - self.value(val2))
                    elif opcode == 'mul':
                        self.write(dst, self.value(val1) * self.value(val2))
                    elif opcode == 'div':
                        self.write(dst, self.value(val1) // self.value(val2))
                    elif opcode == 'mod':
                        self.write(dst, self.value(val1) % self.value(val2))
                    elif opcode == 'cmp':
                        v1 = self.value(val1)
                        v2 = self.value(val2)
                        if v1 < v2:
                            self.write(dst, 1)
                        elif v1 > v2:
                            self.write(dst, -1)
                        else:
                            self.write(dst, 0)

        return None

    def run (self):
        try:
            max_ip = len(self._code)
            self._reg[self.__sp] = self._ram._size # init stack pointer
            self._reg[self.__ra] = max_ip # init return address
            self._ip = 0 # init instruction pointer
            while self._ip >= 0 and self._ip < max_ip:
                ip = self.cycle(self._ip)
                if ip is not None:
                    self._ip = ip
                else:
                    self._ip += 1
                self._probe.read(self._ram.get_activity())
                self._probe.read(self._reg.get_activity())
                self._probe.output_activity()
                sys.stdout.flush()

        except AddrError as e:
            print('Invalid address ' + str(e.addr) + self.dbg(self._ip))
        except ValError as e:
            print('Invalid value ' + str(e.val) + self.dbg(self._ip))
        except WriteError:
            print('Invalid write ' + self.dbg(self._ip))

    def dbg (self, ip):
        return (' on line ' + str(self._code[ip][1][1]) +
                ' of file ' + self._code[ip][1][0])
