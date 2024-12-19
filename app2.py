import gradio as gr

def predict(text, request: gr.Request):
    headers = request.headers
    host = request.client.host
    user_agent = gr.Request.session_hash
    return {
        "ip": host,
        "user_agent": user_agent,
        "headers": headers,
    }

def predi(request: gr.Request,a=1):
    headers = request.headers
    host = request.client.host
    user_agent = gr.Request.session_hash
    return {
        "ip": host,
        "user_agent": user_agent,
        "headers": headers,
        "a":a
    }

with gr.Blocks() as demo:
    b = gr.Button()
    o = gr.Textbox()
    b.click(predi,inputs=2,outputs=o)

demo.launch()