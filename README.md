# BrainXBench-Generation 🚀🧠

Welcome to **BrainXBench-Generation**! This repository is designed to streamline the generation and handling of BrainXBench data. Below, you'll find everything you need to understand, set up, and use this repository effectively. 

**⚠️ This Repo is still under developing, some function(especially for new_bench generation)**

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

### 1️⃣ Loading Data[Currently we are using BXB-Backward & BXB-Forward-v0.6]

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

## Generating New Data

### 1️⃣ Generate Raw Split and Flip results with LLM(GPT-4o)
To generate BrainXBench-Backward, use:
```bash
python generate_BrainX.py --task_type CHOICE --bookname Koch --bench_type backward --BackQS_num 10
```
And for BrainXBench-Forward
```bash
python generate_BrainX.py --bench_type forwards
```

### 2️⃣ Validate LLM's modification
```bash
python python validate_BrainX.py -V your_bench_version -pv your_prompt_for_validation.md
```

### 3️⃣ From RAW file to BenchData
```bash
python load_brainXbench.py -V 0.6
```

### 4️⃣ Pack data to: csv | parquet | json
```bash
python data_packer.py -V your_bench_version
```


## 📌 Contribution
Feel free to contribute! Fork the repo, make changes, and submit a pull request. Let's build something great together! 🚀




## 📝 License
This project is licensed under the YOU-KNOW-WHO License.

---




Happy coding! 💡✨