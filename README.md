# BrainXBench-Generation

Welcome to the **BrainXBench-Generation** repository! This project is designed for the efficient generation, validation, and management of BrainXBench datasets.

> ⚠️ **Note:** This repository is under active development. Some functionalities—especially those related to benchmark auto-generation—may still be evolving.

---

## 📁 Project Structure

Here's an overview of the key components in this repository:

- `Benches/`: Pre-generated benchmark datasets and related resources.
- `configs/`: Configuration files for controlling different stages of the pipeline.
- `data/`: Storage directory for raw, intermediate, and processed data.
- `prompts/`: Prompt templates used during data generation.
- `unused/`: Deprecated or archived scripts for reference.
- `workspaces/`: Workspace-specific files, logs, and outputs.
- `.env`: Defines environment-specific variables.
- `build_bench.py`: Script for constructing benchmark datasets from processed data.
- `collector.py`: Collects data from external sources such as PubMed.
- `flip_result.py`: Flips QA labels (used for contrastive or backward tasks).
- `generate_BrainX.py`: Main script for generating BrainX datasets.
- `infos.py`: Contains constants and shared metadata.
- `run_forward.sh`: Shell script for forward benchmark generation.
- `validate_and_segment.py`: Validates and segments collected raw data.
- `validate_flip.py`: Validates flipped (e.g. backward) results.
- `utils.py`: Utility functions shared across the codebase.

---

## 🚀 Getting Started

Follow these steps to get started with BrainXBench-Generation on your local machine.

### 🔧 Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/spidermonk7/BrainXBench-Generation.git
   cd BrainXBench-Generation
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Set environment variables:**

   Create a `.env` file in the root directory and define the following variables:

   ```env
   # For data collection
   NCBI_API_KEY=your_ncbi_api_key
   BASE_URL=https://eutils.ncbi.nlm.nih.gov/entrez/eutils/

   # For LLM-based generation
   OPENAI_API_KEY=your_openai_api_key
   OPENAI_BASE_URL=https://your-provider-endpoint
   ```

   You can refer to `.env.example` for a complete template.

---

## ⚙️ Configuration

All pipeline components are controlled via a unified configuration file:

- `configs/config.yaml`: Main configuration file that defines queries, threading, paths, and generation parameters.
- Please ensure `config.yaml` is correctly set before running any script.
- A reference file `config.example.yaml` is provided to explain each field.
- Support for multiple optional configs will be added in a future update.

---

## 🧠 Usage: Automated Workflows

You can run the full forward or backward benchmark pipeline with a single command:

### ▶️ Forward Benchmark

```bash
chmod +x run_forward.sh
./scripts/run_forward.sh
```

### ◀️ Backward Benchmark

```bash
chmod +x run_backward.sh
./scripts/run_backward.sh
```

These scripts will sequentially run all required steps based on your configuration.

---

## 📬 Contact

If you have any questions, suggestions, or encounter issues, feel free to:

- Open an issue on the [GitHub repository](https://github.com/spidermonk7/BrainXBench-Generation/issues)
- Or contact the repository owner directly.

---

*🗓️ This README reflects the current status of the project as of **March 29, 2025**. For the latest changes, please refer to the repository.*

---
