import gradio as gr
from instruction import Instruction

def process(text, mode, comment_symbol):
    result = ''
    instructions = text.split('\n')
    
    for instruction in instructions:
        if instruction in ['','\n'] or instruction.find(comment_symbol) == 0: 
            continue
        try:
            code = Instruction(instruction, comment_symbol).assemble(mode)
        except ValueError as e:
            code = str(e)
        result += code + '\n'

    return result

def webui():
    instruction = gr.Textbox(label="Instruction", lines=10, value='ori $1, $1, 0x0101 \nsllv $2, $2, $7')
    machine_code = gr.Textbox(label="Machine Code", lines=10)
    mode = gr.Radio(label="Mode", choices=["bin", "hex"], value="hex")
    comment_symbol = gr.Textbox(label="Comment Symbol", value="//")
    interface = gr.Interface(
        fn=process,
        inputs=[instruction,  mode, comment_symbol],
        outputs=machine_code,
    )
    interface.launch()

if __name__ == "__main__":
    webui()