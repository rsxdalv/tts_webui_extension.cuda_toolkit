import setuptools

setuptools.setup(
    name="tts_webui_extension.cuda_toolkit",
    packages=setuptools.find_namespace_packages(),
    version="0.0.1",
    author="Your Name",
    description="A template extension for TTS Generation WebUI",
    url="https://github.com/yourusername/extension_cuda_toolkit",
    project_urls={},
    scripts=[],
    install_requires=[
        # Add your dependencies here
        # "numpy",
        # "torch",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

