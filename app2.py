import gradio as gr
color1 = ""
color2 = ""
with gr.Blocks() as demo:
    input = gr.Checkbox()
    o1 = gr.ColorPicker(value=color1)
    o2 = gr.ColorPicker(value=color2) 
    @gr.render(inputs=input)
    def show_split(check):
        global color2
        global color1
        global o1
        global o2       
        def of1(input):
            print(input)
            return gr.update(value=input)
        def of2(input):
            print(input)
            return gr.update(value=input)
        def of11(input):
            global color1 
            color1 = input
            return None
        def of12(input):
            global color2 
            color2 = input
            return None
        if check:
            o1.input(of1,o1,o2)
            o2.input(of2,o2,o1)
        else:
            o1.input(of11,o1)
            o2.input(of12,o2)
            pass

demo.launch()
