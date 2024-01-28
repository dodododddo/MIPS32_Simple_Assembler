# MIPS32 Simple Assembler for OpenMIPS (Implemented in Python)
While learning OpenMIPS, I find it cumbersome to write complete assembly files, configure the GNU toolchain, and follow the textbook's methods for translating a few instructions into machine code during the early stages of learning. This small tool can translate MIPS32 instructions in text format into machine code. As I have only studied up to Chapter 7, I have currently tested the instructions covered in the first six chapters.
#### usage

* webui
```
pip install gradio
```
```
python webui.py
```
* file
```
pip install argparse
```
```
python mips_assembler.py --input [$YOUR_INPUT_FILE_PATH] 
                         --output [$YOUR_OUTPUT_FILE_PATH] 
                         --mode ['hex' or 'bin'] 
                         --comment [$YOUR_COMMENT_SYMBOL (such as '//', '#')]
```
Before usage, ensure that the format of your instruction file is similar to example.txt; independent line comments, inline comments, and empty lines will not affect the results.

#### test
```
python instruction.py
```



#### TODO
- [ ] Support all instructions covered in Chapter 7 to Chapter 11. (Now: Ch7.4)
- [x] Simplify the usage based on Gradio
