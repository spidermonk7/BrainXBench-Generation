# BrainXBench-Generation 🚀🧠

Welcome to **BrainXBench-Generation**! This repository is designed to streamline the generation and handling of BrainXBench data. Below, you'll find everything you need to understand, set up, and use this repository effectively. 

## 📂 Project Structure

| File/Folder | Description |
|------------|-------------|
| `Benches/` | Contains benchmark datasets and relevant files. 📊 |
| `data/` | Stores initial dataset files. 📁 |
| `prompts/` | Holds prompt templates for data generation. 📝 |
| `collector.py` | Handles data collection processes. 🏗️ |
| `data_packer.py` | Manages data packaging and organization. 📦 |
| `generate_BrainX.py` | Generates BrainX data from raw inputs. 🔄 |
| `infos.py` | Stores metadata and configuration info. ℹ️ |
| `load_brainXbench.py` | Implements the new loading method. 🚀 |
| `raw_data.py` | Manages raw input data. 🗂️ |
| `utils.py` | Contains utility functions for processing. 🛠️ |
| `README.md` | This file! Explains how to use the repo. 📖 |

## 🛠️ Installation

To get started, clone this repository and install dependencies:

```bash
# Clone the repository
git clone https://github.com/your_username/BrainXBench-Generation.git
cd BrainXBench-Generation

# Install required packages
pip install -r requirements.txt
```

## 🚀 Usage

### 1️⃣ Loading Data

Use the `load_brainXbench.py` script to load data efficiently:

```python
from load_brainXbench import load_data

data = load_data("data/sample_dataset.npy")
print("Data Loaded Successfully!", data.shape)
```

### 2️⃣ Generating New Data

To generate BrainXBench data, use:

```bash
python generate_BrainX.py --input raw_data/sample_input.npy --output data/generated_output.npy
```

### 3️⃣ Packaging Data

Organize and pack data using `data_packer.py`:

```python
from data_packer import pack_data

pack_data("data/generated_output.npy", "Benches/packed_data.zip")
```

## 📌 Contribution
Feel free to contribute! Fork the repo, make changes, and submit a pull request. Let's build something great together! 🚀

## 📝 License
This project is licensed under the MIT License.

---

Happy coding! 💡✨