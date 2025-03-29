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

### Prerequisites

Ensure you have the following installed:

- Python 3.x
- pip (Python package installer)

### Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/spidermonk7/BrainXBench-Generation.git
   cd BrainXBench-Generation
   ```

2. **Install Dependencies:**

   It's recommended to use a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

   Then, install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up Environment Variables:**

   Create a `.env` file in the root directory to store your environment-specific variables. Refer to the `.env.example` file for guidance on the required variables.

### Configuration

Configuration settings are managed using YAML files located in the `configs/` directory. Key configuration files include:

- `config.yaml`: Main configuration file containing parameters such as query terms, database settings, threading options, and API keys.

   Example structure:

   ```yaml
   query: neuroscience
   max_results: 50
   db: pubmed
   threads: 5
   api_key: YOUR_NCBI_API_KEY
   ```

- `journals.yaml`: Lists of journals and related information.

   Example structure:

   ```yaml
   JOURNALS:
     - "Nature Communications"
     - "The Journal of Neuroscience: The Official Journal of the Society for Neuroscience"
     - "Proceedings of the National Academy of Sciences of the United States of America"
     # Add more journals as needed
   ```

- `books.yaml`: Information about books and their chapter ranges.

   Example structure:

   ```yaml
   BOOKS:
     - name: "Biophysics of Computation: Information Processing in Single Neurons"
       chapters: [[30, 49], [50, 73], [74, 109]]
       pdf_path: "data/neuroscience/books/pdfs/Biophysics_of_Computation.pdf"
       source_path: "data/neuroscience/books/Biophysics_of_Computation"
     # Add more books as needed
   ```

Ensure that these configuration files are correctly set up before running the scripts.

### Usage

1. **Data Collection:**

   To collect data based on the configurations:

   ```bash
   python collector.py
   ```

   This script fetches articles from specified databases (e.g., PubMed) based on the query parameters defined in `config.yaml`.

2. **Data Validation and Segmentation:**

   After collecting data, validate and segment it appropriately:

   ```bash
   python validate_and_segment.py
   ```

3. **Benchmark Generation:**

   To generate the BrainX benchmark datasets:

   ```bash
   python generate_BrainX.py
   ```

4. **Automated Workflow:**

   For a streamlined process, you can execute the entire workflow using the provided shell script:

   ```bash
   ./run_forward.sh
   ```

   Ensure that the script has execute permissions:

   ```bash
   chmod +x run_forward.sh
   ```

## Contributing

We welcome contributions to enhance the functionality and efficiency of BrainXBench-Generation. To contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/YourFeature`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Open a pull request.

Please ensure that your contributions align with the project's coding standards and include appropriate documentation.

## License

This project is licensed under the YOU-KNOW-WHO liscense. You are free to use, modify, and distribute this software in accordance with the license terms.

## Contact

For questions, suggestions, or issues, please open an issue on the [GitHub repository](https://github.com/spidermonk7/BrainXBench-Generation/issues) or contact the repository owner directly.

---

*Note: This README reflects the current state of the repository as of March 29, 2025. For the latest updates and changes, please refer to the repository directly.* 