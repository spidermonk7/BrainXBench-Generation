# BrainXBench-Generation

Welcome to the **BrainXBench-Generation** repository! This project is dedicated to the efficient generation and management of BrainXBench datasets. Below, you'll find comprehensive information to help you understand, set up, and utilize this repository effectively.

**⚠️ Note:** This repository is currently under active development. Some functionalities, particularly those related to new benchmark generation, may be incomplete or undergoing changes.

## Project Structure

The repository is organized as follows:

- `Benches/`: Contains benchmark datasets and relevant resources.
- `configs/`: Stores configuration files for various scripts and processes.
- `data/`: Directory for storing raw and processed data files.
- `prompts/`: Includes prompt templates used in data generation.
- `unused/`: Archive of unused or deprecated scripts and files.
- `workspaces/`: Contains workspace-specific files and settings.
- `.env`: Environment variable definitions.
- `.gitignore`: Specifies files and directories to be ignored by Git.
- `README.md`: This document.
- `build_bench.py`: Script for constructing benchmark datasets.
- `collector.py`: Collects data from specified sources.
- `flip_result.py`: Processes and flips result data as needed.
- `generate_BrainX.py`: Main script for generating BrainX datasets.
- `infos.py`: Contains information constants and configurations.
- `requirements.txt`: Lists required Python packages.
- `run_forward.sh`: Shell script to execute a sequence of operations.
- `utils.py`: Utility functions used across various scripts.
- `validate_and_segment.py`: Validates and segments data appropriately.
- `validate_flip.py`: Validates flipped data results.

## Getting Started

To set up and run this project on your local machine, follow these steps:

### Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/spidermonk7/BrainXBench-Generation.git
   cd BrainXBench-Generation
   ```

2. **Install Dependencies:**
    ```
   pip install -r requirements.txt
   ```

3. **Set Up Environment Variables:**

   Create a `.env` file in the root directory to store your environment-specific variables. Refer to the `.env.example` file for guidance on the required variables.

    For benchmark auto-generation task, the variables below are required:
    ```
    NCBI_API_KEY = YOUR_NCBI_API_KEY
    BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"


    OPENAI_API_KEY = YOUR_OPENAI_API_KEY
    OPENAI_BASE_URL= OPENAI_BASE_URL
    ```

### Configuration

Configuration settings are managed using YAML files located in the `configs/` directory. Key configuration files include:

- `config.yaml`: Main configuration file containing parameters such as query terms, database settings, threading options.

- All codes are running based on `config.yaml`, make sure you are using the correct config(we will support optional configs in later version).

- You can refer to `config.example.yaml` for explanation of each configuration.

### Usage: **Automated Workflow**

   For a streamlined forward-benchmark generating process, you can execute the entire workflow using the provided shell script:

   ```bash
   ./run_forward.sh
   ```

   Ensure that the script has execute permissions:

   ```bash
   chmod +x run_forward.sh
   ```
   and backward bench is just the same:
   
   ```bash
   ./run_backward.sh
   ```

## Contact

For questions, suggestions, or issues, please open an issue on the [GitHub repository](https://github.com/spidermonk7/BrainXBench-Generation/issues) or contact the repository owner directly.

---

*Note: This README reflects the current state of the repository as of March 29, 2025. For the latest updates and changes, please refer to the repository directly.* 