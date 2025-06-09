import gradio as gr
import subprocess
import platform


def install_cuda_toolkit(cuda_version):
    """Install CUDA toolkit using conda/micromamba"""
    try:
        # Determine which command to use (micromamba or conda)
        if shutil.which("micromamba"):
            cmd = "micromamba"
        elif shutil.which("conda"):
            cmd = "conda"
        else:
            return "Error: Neither micromamba nor conda found in PATH"

        # Build the installation command
        install_cmd = f"{cmd} install -y -c nvidia -c pytorch -c conda-forge nvidia/label/cuda-{cuda_version}::cuda-toolkit"

        # Run the installation command
        process = subprocess.Popen(
            install_cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        stdout, stderr = process.communicate()

        if process.returncode == 0:
            return f"CUDA Toolkit {cuda_version} installed successfully.\n\n{stdout}"
        else:
            return f"Error installing CUDA Toolkit {cuda_version}:\n{stderr}"

    except Exception as e:
        return f"An error occurred: {str(e)}"


def check_cuda_version():
    """Check current CUDA version if available"""
    try:
        result = subprocess.run(["nvcc", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout
        else:
            return "CUDA not found or not properly installed."
    except FileNotFoundError:
        return "CUDA not found or not properly installed."


def cuda_toolkit_ui():
    gr.Markdown(
        """
    # CUDA Toolkit
    
    This extension helps you install the correct CUDA toolkit for your GPU using conda/micromamba.
    
    ## System Information
    """
    )

    # Display system information
    system_info = gr.Textbox(
        value=f"OS: {platform.system()} {platform.release()}\nPython: {platform.python_version()}",
        label="System Information",
        interactive=False,
    )

    # Check current CUDA version
    current_cuda = gr.Textbox(
        value=check_cuda_version(), label="Current CUDA Installation", interactive=False
    )

    # CUDA version selection
    cuda_version = gr.Dropdown(
        choices=["12.8.0", "12.4.0", "12.1.0", "11.8.0", "11.7.0"],
        value="12.8.0",
        label="CUDA Version",
    )

    # Install button
    install_button = gr.Button("Install CUDA Toolkit")
    output = gr.Textbox(label="Output", lines=10)

    # Connect the button to the installation function
    install_button.click(
        fn=install_cuda_toolkit,
        inputs=[cuda_version],
        outputs=[output],
        api_name="install_cuda_toolkit",
    )

    # Add refresh button to check CUDA version again
    refresh_button = gr.Button("Refresh CUDA Version")
    refresh_button.click(fn=check_cuda_version, inputs=[], outputs=[current_cuda])

    gr.Markdown(
        """
    ## Notes
    - CUDA 12.4+ is required for PyTorch 2.7.0 and later
    """
    )


def extension__tts_generation_webui():
    cuda_toolkit_ui()

    return {
        "package_name": "extension_cuda_toolkit",
        "name": "CUDA Toolkit",
        "requirements": "git+https://github.com/rsxdalv/extension_cuda_toolkit@main",
        "description": "Install and manage CUDA Toolkit for GPU acceleration",
        "extension_type": "interface",
        "extension_class": "tools",
        "author": "NVIDIA",
        "extension_author": "rsxdalv",
        "license": "MIT",
        "website": "https://developer.nvidia.com/cuda-toolkit",
        "extension_website": "https://github.com/rsxdalv/extension_cuda_toolkit",
        "extension_platform_version": "0.0.1",
    }


if __name__ == "__main__":
    import shutil

    if "demo" in locals():
        locals()["demo"].close()
    with gr.Blocks() as demo:
        with gr.Tab("CUDA Toolkit", id="cuda_toolkit"):
            cuda_toolkit_ui()

    demo.launch(
        server_port=7772,  # Change this port if needed
    )
