# VaultGemma Installation Guide

This guide provides detailed installation instructions for VaultGemma with different configurations and use cases.

## Table of Contents

1. [Quick Start](#quick-start)
2. [Organized Dependencies](#organized-dependencies)
3. [Provider-Specific Installation](#provider-specific-installation)
4. [Development Setup](#development-setup)
5. [Troubleshooting](#troubleshooting)

## Quick Start

### Prerequisites

- Python 3.8 or higher
- Git (for installing the VaultGemma-specific transformers version)

### Basic Installation

```bash
# Clone the repository
git clone https://github.com/your-username/VaultGemma.git
cd VaultGemma

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate

# Install core dependencies
pip install -r requirements/core.txt

# Install VaultGemma-specific transformers
pip install git+https://github.com/huggingface/transformers@v4.56.1-Vault-Gemma-preview

# Install in development mode
pip install -e .
```

## Organized Dependencies

VaultGemma provides organized dependency files for different use cases:

### Core Dependencies (`requirements/core.txt`)

Essential dependencies required for basic VaultGemma functionality:

```bash
pip install -r requirements/core.txt
```

**Includes:**
- `torch>=2.0.0` - PyTorch for model inference
- `transformers>=4.56.1` - Hugging Face transformers library
- `huggingface-hub>=0.34.0` - Hugging Face Hub integration
- `tokenizers>=0.22.0` - Text tokenization
- `accelerate>=1.0.0` - Model acceleration
- `sentencepiece>=0.2.1` - SentencePiece tokenizer
- `blobfile>=3.1.0` - File handling

### Provider Dependencies (`requirements/providers.txt`)

Optional dependencies for specific providers:

```bash
pip install -r requirements/providers.txt
```

**Includes:**
- `kagglehub>=0.3.13` - Kaggle model hub
- `kaggle>=1.5.16` - Kaggle API client

### Development Dependencies (`requirements/dev.txt`)

Dependencies for development and testing:

```bash
pip install -r requirements/dev.txt
```

**Includes:**
- `pytest>=7.0.0` - Testing framework
- `pytest-asyncio>=0.21.0` - Async testing support
- `pytest-cov>=4.0.0` - Coverage reporting
- `black>=23.0.0` - Code formatting
- `flake8>=6.0.0` - Linting
- `mypy>=1.0.0` - Type checking
- `isort>=5.12.0` - Import sorting

### Optional Dependencies (`requirements/optional.txt`)

Enhanced features and tools:

```bash
pip install -r requirements/optional.txt
```

**Includes:**
- `huggingface_hub[cli]>=0.34.0` - CLI enhancements
- `jupyter>=1.0.0` - Jupyter notebook support
- `ipywidgets>=8.0.0` - Interactive widgets
- `psutil>=5.9.0` - System monitoring
- `memory-profiler>=0.61.0` - Memory profiling

## Provider-Specific Installation

### Hugging Face Only (Default)

```bash
# Core dependencies (includes Hugging Face support)
pip install -r requirements/core.txt

# Install VaultGemma-specific transformers
pip install git+https://github.com/huggingface/transformers@v4.56.1-Vault-Gemma-preview

# Install VaultGemma
pip install -e .
```

### Kaggle Support

```bash
# Core + Kaggle dependencies
pip install -r requirements/core.txt -r requirements/providers.txt

# Install VaultGemma-specific transformers
pip install git+https://github.com/huggingface/transformers@v4.56.1-Vault-Gemma-preview

# Install VaultGemma
pip install -e .
```

### Using pyproject.toml Extras

```bash
# Core installation
pip install -e .

# With Kaggle support
pip install -e ".[kaggle]"

# With CLI enhancements
pip install -e ".[cli]"

# With Jupyter support
pip install -e ".[jupyter]"

# With monitoring tools
pip install -e ".[monitoring]"

# All optional features
pip install -e ".[all]"

# Development setup
pip install -e ".[dev]"

# Combined extras
pip install -e ".[kaggle,dev,cli]"
```

## Development Setup

### Full Development Environment

```bash
# Clone repository
git clone https://github.com/your-username/VaultGemma.git
cd VaultGemma

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install all dependencies
pip install -r requirements/core.txt
pip install -r requirements/providers.txt
pip install -r requirements/dev.txt
pip install -r requirements/optional.txt

# Install VaultGemma-specific transformers
pip install git+https://github.com/huggingface/transformers@v4.56.1-Vault-Gemma-preview

# Install in development mode
pip install -e .

# Run tests
python run_test.py

# Run examples
python run_example.py starter hello_world
```

### Using pyproject.toml for Development

```bash
# Install with all development dependencies
pip install -e ".[dev,all]"

# Run tests
python run_test.py

# Format code
black src/ tests/

# Lint code
flake8 src/ tests/

# Type check
mypy src/
```

## Installation Verification

### Test Basic Installation

```bash
# Run hello world example
python run_example.py starter hello_world
```

### Test Hugging Face Provider

```bash
# Run Hugging Face example
python run_example.py hf basic
```

### Test Kaggle Provider (if installed)

```bash
# Run Kaggle authentication setup
python run_example.py kaggle auth_setup
```

## Troubleshooting

### Common Issues

1. **ModuleNotFoundError for transformers**
   ```bash
   # Make sure you install the VaultGemma-specific version
   pip install git+https://github.com/huggingface/transformers@v4.56.1-Vault-Gemma-preview
   ```

2. **CUDA/GPU Issues**
   ```bash
   # Install CPU-only PyTorch
   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
   ```

3. **Kaggle Authentication Errors**
   ```bash
   # Set up Kaggle credentials
   python run_example.py kaggle auth_setup
   ```

4. **Memory Issues**
   - Use smaller models
   - Reduce batch sizes
   - Use CPU instead of GPU

### Getting Help

- Check the [Issues](https://github.com/your-username/VaultGemma/issues) page
- Create a new issue with detailed information
- Include your Python version, operating system, and error messages

## Alternative Installation Methods

### Using pip directly

```bash
# Install from main requirements file
pip install -r requirements.txt

# Install everything at once
pip install -r requirements/core.txt -r requirements/providers.txt -r requirements/optional.txt
```

### Using conda (if available)

```bash
# Create conda environment
conda create -n vaultgemma python=3.8
conda activate vaultgemma

# Install PyTorch via conda
conda install pytorch torchvision torchaudio cpuonly -c pytorch

# Install other dependencies via pip
pip install -r requirements/core.txt
```

## Next Steps

After installation, check out the [Examples](README.md#examples) section to get started with VaultGemma!
