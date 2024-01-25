import re
from typing import Literal

register = {f'${i}':i for i in range(32)}

class Instruction(object):
    RTYPE = ['add', 'addu', 'sub', 'subu', 'and', 'or', 'xor', 'nor', 'slt', 'sltu', 'srlv', 'srav', 'sllv', 'movn', 'movz']
    ITYPE = ['addi', 'addiu', 'andi', 'ori', 'xori', 'slti', 'sltiu', 'beq', 'bne']
    JTYPE = ['j', 'jal']
    SPECIAL = ['lui', 'lw', 'sw', 'mthi', 'mtlo', 'mfhi', 'mflo', 'jr', 'nop', 'ssnop', 'sync', 'pref','syscall', 'sll', 'srl', 'sra', 'sllv', 'srlv', 'srav']
    FUNC_CODE_MAP = {
        'add': '100000',
        'addu': '100001',
        'sub': '100010',
        'subu': '100011',
        'and': '100100',
        'or': '100101',
        'xor': '100110',
        'nor': '100111',
        'slt': '101010',
        'sltu': '101011',
        'srlv': '000110',
        'srav': '000111',
        'sllv': '000100',
        'sll': '000000',
        'srl': '000010',
        'sra': '000011',
        'movn': '001011',
        'movz': '001010',
        'jr': '001000',
        'mthi': '010001',
        'mtlo': '010011',
        'mfhi': '010000',
        'mflo': '010010',
        'sync': '001111',
        'nop': '000000',
        'ssnop': '000000',
    }

    OPCODE_MAP = {
        'addi': '001000',
        'addiu': '001001',
        'andi': '001100',
        'ori': '001101',
        'xori': '001110',
        'slti': '001010',
        'sltiu': '001011',
        'beq': '000100',
        'bne': '000101',
        'j': '000010',
        'jal': '000011',
        'lui': '001111',
        'lw': '100011',
        'sw': '101011',
        'sll': '000000',
        'srl': '000000',
        'sra': '000000',
        'mthi': '000000',
        'mtlo': '000000',
        'mfhi': '000000',
        'mflo': '000000',
        'jr': '000000',
        'nop': '000000',
        'ssnop': '000000',
        'sync': '000000',
        'pref': '110011',
        'syscall': '000000'
    }
    

    def __init__(self, instruction, comment_symbol='//'):
        if(instruction == ''):
            raise ValueError('expect instruction but got empty')
        
        self.items = self.parse(instruction, comment_symbol)
        
        if len(self.items) == 0:
            raise ValueError(f'Invalid instruction: {instruction}')
        
        self.op = self.items[0]
        self.type: Literal['R', 'I', 'J', 'SPECIAL']

        if self.op in self.RTYPE:
            self.type = 'R'
        elif self.op in self.ITYPE:
            self.type = 'I'
        elif self.op in self.JTYPE:
            self.type = 'J'
        elif self.op in self.SPECIAL:
            self.type = 'SPECIAL'
        else:
            raise ValueError(f'Unsupported instruction: {instruction}')
        
        match self.type:
            case 'R':
                self.opcode = '000000'
                self.func_code = self.FUNC_CODE_MAP[self.op]
                self.rd = '{:05b}'.format(register[self.items[1]])
                if(self.op in ['sllv', 'srlv', 'srav']):
                    self.rt = '{:05b}'.format(register[self.items[2]])
                    self.rs = '{:05b}'.format(register[self.items[3]])
                else:
                    self.rs = '{:05b}'.format(register[self.items[2]])
                    self.rt = '{:05b}'.format(register[self.items[3]])
                
                self.mechine_code = f'{self.opcode}{self.rs}{self.rt}{self.rd}00000{self.func_code}'

            case 'I':
                self.opcode = self.OPCODE_MAP[self.op]
                self.rt = '{:05b}'.format(register[self.items[1]])
                self.rs = '{:05b}'.format(register[self.items[2]])
                self.imm = '{:016b}'.format(int(self.items[3], 16))
                self.mechine_code = f'{self.opcode}{self.rs}{self.rt}{self.imm}'

            case'J':
                self.opcode = self.OPCODE_MAP[self.op]
                self.address = '{:026b}'.format(int(self.items[1], 16))
                self.mechine_code = f'{self.opcode}{self.address}'

            case 'SPECIAL':
                self.opcode = self.OPCODE_MAP[self.op]
                match self.op:
                    case 'lui':
                        self.rt = '{:05b}'.format(register[self.items[1]])
                        self.imm = '{:016b}'.format(int(self.items[2], 16))
                        self.mechine_code = f'{self.opcode}00000{self.rt}{self.imm}'

                    case 'jr':
                        self.func_code = self.FUNC_CODE_MAP[self.op]
                        self.rs = '{:05b}'.format(register[self.items[1]])
                        self.mechine_code = f'{self.opcode}{self.rs}00000{self.func_code}'

                    case 'lw':
                        self.rt = '{:05b}'.format(register[self.items[1]])
                        self.imm = '{:016b}'.format(int(self.items[2], 16))
                        self.rs = '{:05b}'.format(register[self.items[3]])
                        self.mechine_code = f'{self.opcode}{self.rs}{self.rt}{self.imm}'

                    case 'sw':
                        self.rt = '{:05b}'.format(register[self.items[1]])
                        self.imm = '{:016b}'.format(int(self.items[2], 16))
                        self.rs = '{:05b}'.format(register[self.items[3]])
                        self.mechine_code = f'{self.opcode}{self.rs}{self.rt}{self.imm}'

                    case 'mthi':
                        self.rs = '{:05b}'.format(register[self.items[1]])
                        self.func_code = self.FUNC_CODE_MAP[self.op]
                        self.mechine_code = f'{self.opcode}{self.rs}000000000000000{self.func_code}'

                    case 'mtlo':
                        self.rs = '{:05b}'.format(register[self.items[1]])
                        self.func_code = self.FUNC_CODE_MAP[self.op]
                        self.mechine_code = f'{self.opcode}{self.rs}000000000000000{self.func_code}'

                    case 'mfhi':
                        self.rd = '{:05b}'.format(register[self.items[1]])
                        self.func_code = self.FUNC_CODE_MAP[self.op]
                        self.mechine_code = f'{self.opcode}0000000000{self.rd}00000{self.func_code}'

                    case 'mflo':
                        self.rd = '{:05b}'.format(register[self.items[1]])
                        self.func_code = self.FUNC_CODE_MAP[self.op]
                        self.mechine_code = f'{self.opcode}0000000000{self.rd}00000{self.func_code}'
                    
                    case 'sll':
                        self.opcode = self.OPCODE_MAP[self.op]
                        self.func_code = self.FUNC_CODE_MAP[self.op]
                        self.rd = '{:05b}'.format(register[self.items[1]])
                        self.rt = '{:05b}'.format(register[self.items[2]])
                        self.shamt = '{:05b}'.format(int(self.items[3]))
                        self.mechine_code = f'{self.opcode}00000{self.rt}{self.rd}{self.shamt}{self.func_code}'


                    case 'srl':
                        self.opcode = self.OPCODE_MAP[self.op]
                        self.func_code = self.FUNC_CODE_MAP[self.op]
                        self.rd = '{:05b}'.format(register[self.items[1]])
                        self.rt = '{:05b}'.format(register[self.items[2]])
                        self.shamt = '{:05b}'.format(int(self.items[3]))
                        self.mechine_code = f'{self.opcode}00000{self.rt}{self.rd}{self.shamt}{self.func_code}'

                    case 'sra':
                        self.opcode = self.OPCODE_MAP[self.op]
                        self.func_code = self.FUNC_CODE_MAP[self.op]
                        self.rd = '{:05b}'.format(register[self.items[1]])
                        self.rt = '{:05b}'.format(register[self.items[2]])
                        self.shamt = '{:05b}'.format(int(self.items[3]))
                        self.mechine_code = f'{self.opcode}00000{self.rt}{self.rd}{self.shamt}{self.func_code}'

                    case 'nop':
                        self.opcode = self.OPCODE_MAP[self.op]
                        self.func_code = self.FUNC_CODE_MAP[self.op]
                        self.mechine_code = f'{self.opcode}00000000000000000000{self.func_code}'

                    case 'ssnop':
                        self.opcode = self.OPCODE_MAP[self.op]
                        self.func_code = self.FUNC_CODE_MAP[self.op]
                        self.mechine_code = f'{self.opcode}00000000000000000001{self.func_code}'

                    case 'sync':
                        self.opcode = self.OPCODE_MAP[self.op]
                        self.func_code = self.FUNC_CODE_MAP[self.op]
                        self.mechine_code = f'{self.opcode}00000000000000000001{self.func_code}'
                    
                    case 'pref':
                        self.opcode = self.OPCODE_MAP[self.op]
                        self.mechine_code = f'{self.opcode}' + '00000000000000000000000000'
                
    
    def assemble(self, mode: Literal['bin', 'hex'] = 'hex') -> str | None:
        if self.mechine_code == '':
            return None
        if mode not in ['bin', 'hex']:
            raise ValueError(f'Unsupported mode: {mode}')
        elif mode == 'bin':
            return self.mechine_code
        elif mode == 'hex':
            return hex(int(self.mechine_code, 2))[2:].zfill(8)
        
            
    
    @staticmethod
    def parse(instruction, comment_symbol='//'):
        if(instruction == ''):
            raise ValueError('expect instruction but got empty')
        
        # 过滤行尾注释
        symbol_idx = instruction.find(comment_symbol) 
        if symbol_idx != -1:
            instruction = instruction[:symbol_idx]
        if instruction == '':
            raise ValueError('expect instruction but got comment')
        instruction = re.sub(r'[()]', ' ', instruction)
        result = re.split(r'\s|,', instruction)
        result = [item for item in result if item]
        return result
    

if __name__ == '__main__':
    #### test ####
    Instructions = [
        'lui $1 0x0101',
        'ori $1, $1, 0x0101',
        'ori $2, $1, 0x1100',
        'or $1, $1, $2',
        'andi $3, $1, 0x00fe',
        'and $1, $3, $1',
        'xori $4, $1, 0xff00',
        'xor $1, $4, $1', 
        'nor $1, $4, $1',
        'lui $2, 0x0404',
        'ori $2, $2, 0x0404',
        'ori $7, $0, 0x7',
        'ori $5, $0, 0x5',
        'ori $8, $0, 0x8',
        'sync',
        'sll $2, $2, 8',
        'sllv $2, $2, $7',
        'srl $2, $2, 8',
        'srlv $2, $2, $5',
        'nop',
        'pref',
        'sll $2, $2, 19',
        'ssnop',
        'sra $2, $2, 16',
        'srav $2, $2, $8',
        'lui $1, 0x0000',
        'lui $2, 0xffff',
        'lui $3, 0x0505',
        'lui $4, 0x0000',
        'movz $4 $2 $1',
        'movn $4 $3 $1',
        'movn $4 $3 $2',
        'movz $4 $2 $3',
        'mthi $0',
        'mthi $2',
        'mthi $3',
        'mfhi $4',
        'mtlo $3',
        'mtlo $2',
        'mtlo $1',
        'mflo $4'   
    ]

    machine_codes = [
        '3c010101',
        '34210101',
        '34221100',
        '00220825',
        '302300fe',
        '00610824',
        '3824ff00',
        '00810826',
        '00810827',
        '3c020404',
        '34420404',
        '34070007',
        '34050005',
        '34080008',
        '0000004f',
        '00021200',
        '00e21004',
        '00021202',
        '00a21006',
        '00000000',
        'cc000000',
        '000214c0',
        '00000040',
        '00021403',
        '01021007',
        '3c010000',
        '3c02ffff',
        '3c030505',
        '3c040000',
        '0041200a',
        '0061200b',
        '0062200b',
        '0043200a',
        '00000011',
        '00400011',
        '00600011',
        '00002010',
        '00600013',
        '00400013',
        '00200013',
        '00002012'
    ]
    
    assert(len(Instructions) == len(machine_codes))
    fail_msgs = []
    
    for idx, instruct in enumerate(Instructions):
        result = Instruction(instruct).assemble()
        if(result != machine_codes[idx]):
            fail_msg = f'<{idx + 1}> Error: {instruct} -> expected {machine_codes[idx]} but got {result} '
            fail_msgs.append(fail_msg)
            print(fail_msg)
        else:
            print(f'<{idx + 1}> Ok: {instruct} -> {Instruction(instruct).assemble()}')
    
    if fail_msgs:
        print('\nFail:\n')
        for msg in fail_msgs:
            print(msg)

    else:
        print('\nAll Test Pass!')
    


