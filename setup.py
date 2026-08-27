from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="codemesa",
    version="0.1.0",
    description="Multi-agent AI coding assistant that builds complete projects from scratch",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Kamalesh",
    packages=find_packages("src"),
    package_dir={"": "src"},
    install_requires=[
        "click>=8.0",
        "pydantic>=2.0",
    ],
    extras_require={
        "local": ["llama-cpp-python>=0.2"],
        "ollama": ["ollama"],
        "dev": ["pytest>=7.0", "ruff", "mypy"],
    },
    entry_points={
        "console_scripts": [
            "codemesa=src.cli.main:cli",
        ],
    },
    python_requires=">=3.9",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Code Generators",
    ],
)
