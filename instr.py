# #!/usr/bin/env python
# # -*- coding: utf-8 -*-
import linecache

class Instr:

    def split_infos(self, space, contents): # make space betwin differents elements
        text = contents
        size = len(text)
        while size < space:
            text = text + ' '
            size += 1
        return text

    def get_infos (self, program, i):
        takeAll = ''
        file = program[i][1][0]
        line = program[i][1][1]
        # if line < 0:
        #     line = program[i][0][1][1]
        #     file = program[i][1][2]+'.asm'
        code = linecache.getline(file, line)
        code = code.replace('\t','')
        code = code.replace('\n','')
        code = code.split(';', 1)[0].strip()
        takeAll = self.split_infos(30, self.get_program(i,program))+self.split_infos(30, code)+file+':'+str(line)
        return takeAll

    def stack_infos(self, program):
        i = 0
        instrs = []
        for instr in program:
            instrs.append(self.get_infos(program,i))
            i += 1
        instrs.append("")
        return instrs

    def get_program (self, k, program): 
        file = program[k][1][0]
        line = program[k][1][1]
        t = ''
        for i in program[k][0]:
            for j in i:
                if j == 'reg':
                    t = t+' r'
                if j == 'imm':
                    t = t+' #'
                if j == 'mem':
                    t = t+' @'
                if j != 'reg' and j != 'imm' and j != 'mem':
                    t = t+str(j)
                if j == 'ref':
                    t = linecache.getline(file, line)
                    t = t.replace('\t','')
                    t = t.replace('\n','') 
                    t = t.split(';', 1)[0].strip()
                    return t 
        return t
