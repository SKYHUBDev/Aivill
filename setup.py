from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="aivill",
    version="0.1.0",
    author="AiVill Team",
    description="Self-Learning Villain Brain AI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.9",
    install_requires=[],
    extras_require={
        "dev": [],
    },
    entry_points={
        "console_scripts": [
            "aivill=aivill.examples.terminal_demo:main",
        ],
    },
)
