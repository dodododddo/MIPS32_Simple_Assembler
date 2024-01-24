from instruction import Instruction
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', help='Input file path', default='example.txt')
    parser.add_argument('--output', help='Output file path', default='inst_rom.data')
    parser.add_argument('--mode', help='Output mode', choices=['bin', 'hex'], default='hex')
    parser.add_argument('--comment', help='Comment symbol', default='//')
    args = parser.parse_args()

    with open(args.input, 'r') as f, open(args.output, 'w') as g:
        lines = f.readlines()
        for line in lines:
            # Filtering Blank Lines and Comment Lines
            if line in ['','\n'] or line.find(args.comment) == 0:
                continue
            instruction = Instruction(line, args.comment)
            machine_code = instruction.assemble(args.mode)
            if(machine_code != None):
                g.writelines(instruction.assemble(args.mode) + '\n')
        print('assemble done')