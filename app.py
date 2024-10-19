import gradio as gr
import subprocess
from pathlib import Path
import time

def run_command(input_image_path, tile, overlap):
    input_path = Path(input_image_path)
    timestamp = time.time_ns()
    output_file = input_path.with_name(f"{input_path.stem}_{timestamp}_output{input_path.suffix}")
    tile_file = input_path.with_name(f"{input_path.stem}_{timestamp}_output_2x2.jpg")

    command = ["img2texture", str(input_path), str(output_file)]

    if tile:
        command.append("--tile")

    if overlap > 0:
        command.extend(["--overlap", str(overlap)])

    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError:
        return None, "Command failed to execute."

    if tile:
        return (tile_file.resolve(), "Success.") if tile_file.exists() else (None, "Tile output file not found.")
    else:
        return (output_file.resolve(), "Success.") if output_file.exists() else (None, "Output file not found.")

app = gr.Interface(
    fn=run_command,
    inputs=[
        gr.Image(type="filepath", label="Input Image"),
        gr.Checkbox(label="Tile"),
        gr.Slider(minimum=0, maximum=0.5, step=0.001, value=0.25, label="Overlap")
    ],
    outputs=[
        gr.Image(type="filepath", label="Processed Image"),
        gr.Textbox(label="Status Message", lines=2, interactive=False)
    ],
    title="Seam-Stream",
    description="Upload an image, select options, and press 'Send' to process the image.",
    allow_flagging='never'
)

app.launch(server_name="0.0.0.0")