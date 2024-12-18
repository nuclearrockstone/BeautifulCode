import gradio as gr
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import TerminalFormatter
from pygments.formatters import HtmlFormatter

COLOR_BAR    ="rgb(171, 176, 182)"
COLOR_WINDOW ="rgb(243, 243, 243)"

CODE_TEST    = '''
def greet(name):
    print(f'Hello, {name}!')
greet('World')
'''
def Code_Count(line_code):
    '''
    Count the num of line and max line
    '''
    lines = line_code.split('\n')
    return max(len(line) for line in lines)

def Wrap_Code(code,color_bar="rgb(171, 176, 182)",color_window="rgb(243, 243, 243)"):
    print(3)
    formatter = HtmlFormatter(style='colorful', linenos=True,wrapcode=True)
    MAX_CHAR = 15*Code_Count(code)

    CUSTOM_HTML = """
    <div style="width: {0}px; height: 40px; background-color: {1}; border-radius: 1em 1em 0 0; display: flex; align-items: center; justify-content: start; gap: 10px;">
            <div style="width: 20px; height: 20px; background-color: red; border-radius: 50%; margin-left:10px"></div>
            <div style="width: 20px; height: 20px; background-color: green; border-radius: 50%;"></div>
            <div style="width: 20px; height: 20px; background-color: orange; border-radius: 50%;"></div>
    </div>
    """.format(MAX_CHAR,color_bar)
    CUSTOM_CSS  = """
    .normal,.p,.nb,.n,.s1,.sa,.k,.nf{{ 
            font-size:30px;
            height:35px;
    }}
    pre{{
            line-height: 1.5;
    }}
    .highlight{{
            width: {0}px;
            background-color: {1};
            border-bottom-left-radius: 1em;
            border-bottom-right-radius: 1em;   
    }}
    """.format(MAX_CHAR,color_window)

    FORMAT_CSS = formatter.get_style_defs('.highlight')
    FORMAT_CODE = highlight(code, PythonLexer(), formatter)
    FULL_HTML = f"""
    <style>
    {FORMAT_CSS}
    {CUSTOM_CSS}
    </style>
    {CUSTOM_HTML}
    {FORMAT_CODE}
    """
    return FULL_HTML



with gr.Blocks() as beautifulcode:
    with gr.Row():
        with gr.Column():
            input_code = gr.Code(language="python")
            with gr.Group():
                color_follow=gr.Checkbox()
                cp_bar = gr.ColorPicker(value=COLOR_BAR)
                cp_window = gr.ColorPicker(value=COLOR_WINDOW)                
                def Cp_Bar_Fun(code,cp_bar,cp_window,flag):
                    
                    if flag:
                        FULL_HTML = Wrap_Code(code,cp_bar,cp_bar)
                        return FULL_HTML,gr.update(value=cp_bar)
                    else:
                        FULL_HTML = Wrap_Code(code,cp_bar,cp_window)
                        return FULL_HTML,gr.update(value=cp_window)
                def Cp_Window_Fun(code,cp_bar,cp_window,flag):
                    
                    if flag:
                        FULL_HTML = Wrap_Code(code,cp_window,cp_window)
                        return FULL_HTML,gr.update(value=cp_window)
                    else:
                        FULL_HTML = Wrap_Code(code,cp_bar,cp_window)
                        return FULL_HTML,gr.update(value=cp_bar)               
        output = gr.HTML(container=True, show_label=True)
        input_code.change(Wrap_Code,inputs=[input_code,cp_bar,cp_window],outputs=output)
        cp_bar.input(Cp_Bar_Fun,inputs=[input_code,cp_bar,cp_window,color_follow],outputs=[output,cp_window])
        cp_window.input(Cp_Window_Fun,inputs=[input_code,cp_bar,cp_window,color_follow],outputs=[output,cp_bar])

beautifulcode.launch()