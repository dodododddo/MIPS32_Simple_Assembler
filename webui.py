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
    instruction = gr.Textbox(label="Instruction", 
                             value='sll $2, $2, 8\nsllv $2, $2, $7\nsrl $2, $2, 8\nsrlv $2, $2, $5\nnop\n',
                             lines=10)
    machine_code = gr.Textbox(label="Machine Code", lines=10)
    mode = gr.Radio(label="Mode", choices=["bin", "hex"], value="hex")
    comment_symbol = gr.Textbox(label="Comment Symbol", value="//")
    with open('example.txt', 'r') as f:
        example_text = f.readlines()[: 5]

    interface = gr.Interface(
        fn=process,
        inputs=[instruction, mode, comment_symbol],
        outputs=machine_code,
        examples=[[example, 'hex', '//'] for example in example_text],
    )
    
    interface.launch()

if __name__ == "__main__":
    webui()