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

### 1️⃣ Loading Data[Currently we are using BXB-Backward & BXB-Forward-v0.4]

Use the `load_brainXbench.py` script to load data efficiently:

```python
from load_brainXbench import load_brainXbench_forward, load_brainXbench_backward

result_type = "Opposite_Outcome"
assert result_type in ["Opposite_Outcome", "Incorrect_Causal_Relationship", "Factor_Misattribution"]
forward_bench = load_brainXbench_forward(result_type)

question_type = "CHOICE"
mini = True
assert question_type in ["CHOICE", "TEXT", "TF"]
backward_bench = load_brainXbench_backward(question_type, mini) # TF-bench support mini set only!!!

print("🤖: Data Loaded Successfully!")
```

### 2️⃣ Generating New Data

To generate BrainXBench data, use:
*(detail usage coming soon, now run generate_BrainX.py with default setting would generate new BXB-forward)*
```bash
python generate_BrainX.py 
```

### 3️⃣ Packaging Data

Organize and pack data using `data_packer.py`(This would automatically save csv data to both json and parquet)
    - The packed data file will be saved in the jsons/ and parquets/ folders, alongside the csvs/ folder in the same path.
```python
from data_packer import pack_data

data_path = "Benches/forward/flip/csvs/v_direct0.4.csv"
pack_data(data_path)
```

## 📌 Contribution
Feel free to contribute! Fork the repo, make changes, and submit a pull request. Let's build something great together! 🚀

## 📝 License
This project is licensed under the YOU-KNOW-WHO License.

---

Happy coding! 💡✨