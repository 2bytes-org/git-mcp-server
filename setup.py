from setuptools import setup, find_packages

setup(
    name="mcp-git-server",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "gitpython>=3.1.0",
        "pydantic>=2.0.0",
        "model-context-protocol>=0.3.0"
    ],
    entry_points={
        "console_scripts": [
            "mcp-git-server=mcp_git_server.main:main",
        ],
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="A Model Context Protocol server for Git repository interaction",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/2bytes-org/git-mcp-server",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)