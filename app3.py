import gradio as gr
from html2image import Html2Image
hti = Html2Image(browser="chrome")

def greet(name, intensity,color):
    html="""
    <head>
        <link rel="stylesheet" type="text/css" href="style.css">
    </head>
    <body>
        <h1> Hello world</h1>
        <br /> 
        <h1> by {} </h1>
    </body>
""".format(name)
    hti.size = (1000, 400)
    hti.screenshot(html_str=html,css_file="style.css", save_as='red_page.png')
    return "red_page.png"
    #return "# Hello, " + name + "!" * int(intensity)

demo = gr.Interface(
    fn=greet,
    inputs=["text", gr.Slider(value=2, minimum=0, maximum=20, step=5), gr.Slider(label="color")],
    outputs=[gr.Image(type="filepath")],
)

demo.launch()