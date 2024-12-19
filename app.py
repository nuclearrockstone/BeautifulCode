import gradio as gr
from html2image import Html2Image
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import TerminalFormatter
from pygments.formatters import HtmlFormatter
import re
from colorsys import rgb_to_hls, hls_to_rgb

hti = Html2Image(browser="chrome")

COLOR_BAR    ="rgb(171, 176, 182)"
COLOR_WINDOW ="rgb(243, 243, 243)"

CODE_TEST    = '''
def greet(name):
    print(f'Hello, {name}!')
greet('World')
'''
GRADIO_CUSTOM_CSS = ".gradio-container-5-9-0 .prose table, .gradio-container-5-9-0 .prose tr, .gradio-container-5-9-0 .prose td, .gradio-container-5-9-0 .prose th{border:none}"


def Lighten_Color(rgba_str, factor=0.5):
    match = re.match(r'rgba\(([\d.]+),\s*([\d.]+),\s*([\d.]+),\s*([\d.]+)\)', rgba_str)    
    
    r, g, b, a = map(float, match.groups())   
    r, g, b = r / 255, g / 255, b / 255    
    h, l, s = rgb_to_hls(r, g, b)    
    l = min(1.0, l + (1.0 - l) * factor)
    r, g, b = hls_to_rgb(h, l, s)    
    r, g, b = int(r * 255), int(g * 255), int(b * 255)
    
    return f"rgba({r}, {g}, {b}, {a})"

def Darken_Color(rgba_str, factor=0.3):
    match = re.match(r'rgba\(([\d.]+),\s*([\d.]+),\s*([\d.]+),\s*([\d.]+)\)', rgba_str)    
    
    r, g, b, a = map(float, match.groups())
    r, g, b = r / 255, g / 255, b / 255
    h, l, s = rgb_to_hls(r, g, b)    
    l = max(0.0, l - factor) 
    r, g, b = hls_to_rgb(h, l, s)
    r, g, b = r * 255, g * 255, b * 255
    return f"rgba({r:.2f}, {g:.2f}, {b:.2f}, {a})"

def Code_Count(line_code):
    '''
    Count the num of line and max line
    '''
    lines = line_code.split('\n')
    return max(len(line) for line in lines),len(lines)

def Wrap_Code(code,color_bar="rgb(171, 176, 182)",color_window="rgb(243, 243, 243)"):
    print(3)
    formatter = HtmlFormatter(style='colorful', linenos=True,wrapcode=True)
    MAX_CHAR = 20*Code_Count(code)[0]

    CUSTOM_HTML = """
    <div style="width: {0}px; height: 40px; background-color: {1}; border-radius: 1em 1em 0 0; display: flex; align-items: center; justify-content: start; gap: 10px;">
            <div style="width: 20px; height: 20px; background-color: red; border-radius: 50%; margin-left:10px"></div>
            <div style="width: 20px; height: 20px; background-color: green; border-radius: 50%;"></div>
            <div style="width: 20px; height: 20px; background-color: orange; border-radius: 50%;"></div>
    </div>
    """.format(MAX_CHAR,color_bar)
    CUSTOM_CSS  = """
    .normal,.p,.nb,.n,.s1,.sa,.k,.nf,.hll,.c,.err,.k,.o,.ch,.cm,.cp,.cpf,.c1,.cs,.gd,.ge,.ges,.gr,.gh,.gi,.go,.gp,.gs,.gu,.gt,.kc,.kd,.kn,.kp,.kr,.kt,.m,.s,.na,.nb,.nc,.no,.nd,.ni,.ne,.nf,.nl,.nn,.nt,.nv,.ow,.w,.mb,.mf,.mh,.mi,.mo,.sa,.sb,.sc,.dl,.sd,.s2,.se,.sh,.si,.sx,.sr,.s1,.ss,.bp,.fm,.vc,.vg,.vi,.vm,.il{{ 
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

def Generate_Image(code,color_bar="rgb(171, 176, 182)",color_window="rgb(243, 243, 243)"):
    hti.size = (20*Code_Count(code)[0], 45*Code_Count(code)[1]+60)
    print(45*Code_Count(code)[1]+20)
    hti.screenshot(html_str=Wrap_Code(code,color_bar,color_window),save_as='code.png')
    return 'code.png'

with gr.Blocks(css=GRADIO_CUSTOM_CSS) as beautifulcode:
    with gr.Row(equal_height=True):
        with gr.Column():
            input_code = gr.Code(language="python")
            
            with gr.Row(equal_height=True):
                color_follow=gr.Checkbox()
                cp_bar = gr.ColorPicker(value=COLOR_BAR)
                cp_window = gr.ColorPicker(value=COLOR_WINDOW)                
                def Cp_Bar_Fun(code,cp_bar,cp_window,flag):

                    if flag and code!="":
                        cp_window = Lighten_Color(cp_bar)
                        FULL_HTML = Wrap_Code(code,cp_bar,cp_window)
                        print(cp_bar)
                        return FULL_HTML,gr.update(value=cp_window)
                    elif code!= "":
                        FULL_HTML = Wrap_Code(code,cp_bar,cp_window)
                        return FULL_HTML,gr.update(value=cp_window)
                    else:
                        FULL_HTML = None
                        return FULL_HTML,gr.update(value=cp_window)
                def Cp_Window_Fun(code,cp_bar,cp_window,flag):
                    
                    if flag and code!="":
                        cp_bar = Darken_Color(cp_window)
                        FULL_HTML = Wrap_Code(code,cp_bar,cp_window)
                        return FULL_HTML,gr.update(value=cp_bar)
                    elif code!="":
                        FULL_HTML = Wrap_Code(code,cp_bar,cp_window)
                        return FULL_HTML,gr.update(value=cp_bar)
                    else:
                        FULL_HTML = None
                        return FULL_HTML,gr.update(value=cp_bar)               
        output = gr.HTML(container=True, show_label=True)
        input_code.change(Wrap_Code,inputs=[input_code,cp_bar,cp_window],outputs=output)
        cp_bar.input(Cp_Bar_Fun,inputs=[input_code,cp_bar,cp_window,color_follow],outputs=[output,cp_window])
        cp_window.input(Cp_Window_Fun,inputs=[input_code,cp_bar,cp_window,color_follow],outputs=[output,cp_bar])
    with gr.Row():
        generate = gr.Button()
        image = gr.Image(type="filepath",label="Image")
        generate.click(Generate_Image,inputs=[input_code,cp_bar,cp_window],outputs=image)
    with gr.Row():
        example = gr.Examples([CODE_TEST],input_code)    
beautifulcode.launch()