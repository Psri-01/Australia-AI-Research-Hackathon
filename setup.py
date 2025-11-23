from setuptools import setup, find_packages

setup(
    name="vibe-refinery",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "langgraph",
        "langchain-openai",
        "python-dotenv",
        "streamlit",
        "tqdm"
    ],
    entry_points={
        'console_scripts': [
            'vibe-check=vibe_refinery.main:main',  # Creates a CLI command 'vibe-check'
            'vibe-ui=vibe_refinery.app_launcher:run_ui' # Creates command 'vibe-ui'
        ],
    },
)