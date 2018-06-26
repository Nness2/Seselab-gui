# #!/usr/bin/env python
# # -*- coding: utf-8 -*-
import linecache
import os

class Instr:

    def split_infos(self, space, contents): 
        text = contents
        size = len(text)
        while size < space:
            text = text + ' '
            size += 1
        return text

    def get_infos (self, program, i):

        takeAll = ''
        file = os.path.basename(program[i][1][0])
        line = program[i][1][1]
        code = linecache.getline(file, line)
        code = code.replace('\t','')
        code = code.replace('\n','')
        code = code.split(';', 1)[0].strip()
        takeAll = self.split_infos(25, self.get_program(program[i][0])) + self.split_infos(25, code) + file + ':' + str(line)
        if len(program[i][1]) == 3:
            takeAll += ' (' + program[i][1][2] + ')'
        return takeAll

    def stack_infos(self, program):
        instrs = ['']
        for i in range(1, len(program)):
            instrs.append(self.get_infos(program,i))
        instrs.append("")
        return instrs


    def get_program (self, program):
        t = ''
        for i in program:
            for j in i:
                if j == 'reg':
                    t = t+' r'
                if j == 'imm':
                    t = t+' #'
                if j == 'mem':
                    t = t+' @'
                if j != 'reg' and j != 'imm' and j != 'mem':
                    t = t+str(j)
        return t
        
    # def get_program (self, program):
    #     text = ''
    #     for i in program:
    #         if i[0] is not None:
    #             text = self.get_program (i) + text
    #         else:
    #             if i == 'reg':
    #                 return ' r'
    #             elif i == 'imm':
    #                 return ' #'
    #             elif i == 'mem':
    #                 return ' @'
    #             elif i == 'ref':
    #                 return ' !'
    #             else:
    #                 return str(i)
    #     return str(text)
