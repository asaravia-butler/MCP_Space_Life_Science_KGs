from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="mcp-space-life-sciences",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Integrated MCP server for GeneLab, PrimeKG, and SPOKE-OKN knowledge graphs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/YOUR-USERNAME/MCP_Space_Life_Science_KGs",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.10",
    install_requires=[
        "mcp>=0.1.0",
        "pandas>=2.0.0",
        "numpy>=1.24.0",
        "neo4j>=5.0.0",
        "SPARQLWrapper>=2.0.0",
        "matplotlib>=3.7.0",
        "seaborn>=0.12.0",
        "networkx>=3.0",
        "matplotlib-venn>=0.11.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
            "jupyter>=1.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "mcp-space-life-sciences=mcp_space_life_sciences.server:main",
        ],
    },
)
