import gradio as gr
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import TerminalFormatter
from pygments.formatters import HtmlFormatter

CODE_TEST = '''
def greet(name):
    print(f'Hello, {name}!')
greet('World')
'''
def code_count(line_code):
    '''
    Count the num of line and max line
    '''
    lines = line_code.split('\n')
    return max(len(line) for line in lines)

def wrap_code(code):
    formatter = HtmlFormatter(style='colorful', linenos=True,wrapcode=True)
    MAX_CHAR = 15*code_count(code)
    CUSTOM_HTML = """
    <div style="width: {0}px; height: 40px; background-color: lightgray; border-radius: 1em 1em 0 0; display: flex; align-items: center; justify-content: start; gap: 10px;">
            <div style="width: 20px; height: 20px; background-color: red; border-radius: 50%; margin-left:10px"></div>
            <div style="width: 20px; height: 20px; background-color: green; border-radius: 50%;"></div>
            <div style="width: 20px; height: 20px; background-color: orange; border-radius: 50%;"></div>
    </div>
    """.format(MAX_CHAR)
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
            background-color: #eeeeee;
            border-bottom-left-radius: 1em;
            border-bottom-right-radius: 1em;   
    }}
    """.format(MAX_CHAR)

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
        """ gr.HTML("<h1>Hello</h1>")
        gr.HTML("<h1>Hello</h1>", container=True)
        gr.HTML("<h1>Hello</h1>", container=True, show_label=True) """
        input = gr.Code(language="python")
        output = gr.HTML(container=True, show_label=True)
        """ with gr.Column():
            output1 = gr.Number(label="Row",show_label=True)
            output2 = gr.Number(label="MaxChar",show_label=True)
        output = [output1,output2] """
        input.change(wrap_code,inputs=input,outputs=output)

beautifulcode.launch()