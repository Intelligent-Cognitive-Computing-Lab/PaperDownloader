# Paper Downloader

A command-line Python script to automate the downloading of academic papers from a list of URLs. The script parses a given file for URLs, identifies the host (e.g., arXiv, OpenReview), and downloads the corresponding PDF.

## Features

*   **Configurable Inputs**: Specify the input file and save directory via command-line arguments.
*   **Multi-Site Support**: Automatically handles different download logic for various academic sites.
*   **Intelligent Naming**: Saves PDFs with meaningful names derived from their URLs (e.g., `1706.03762.pdf`).
*   **Robust**: Skips unsupported URLs and handles download failures gracefully.

### Supported Websites
*   arXiv
*   Sci-Hub
*   OpenReview

## Prerequisites

*   Python 3
*   `pip` for installing packages

## Installation

1.  **Clone the repository or download the script:**
    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```
    Or simply save `download.py` to your local machine.

2.  **Install required libraries:**
    ```bash
    pip install requests beautifulsoup4
    ```

## Usage

The script is controlled via the command line.

### Command-Line Arguments

*   `--file FILE`: Specifies the path to the input file containing the list of paper URLs.
    *   **Default**: `papers.md`
*   `--save_dir SAVE_DIR`: Specifies the directory where the downloaded PDF files will be saved. The directory will be created if it doesn't exist.
    *   **Default**: The current directory (`.`)

### Input File Format

The input file (e.g., `papers.md`) must contain one paper URL per line. The script will process each line as a separate URL. Empty lines are ignored.

**Example `papers.md`:**
```
https://arxiv.org/abs/1706.03762
https://openreview.net/forum?id=HkMA2i-R-
https://sci-hub.se/10.1109/5.771073
```

### Examples

1.  **Basic Usage (Default settings)**
    *   Reads URLs from `papers.md`.
    *   Saves PDFs to the current directory.
    ```bash
    python download.py
    ```

2.  **Using a Custom Input File**
    *   Reads URLs from `my_reading_list.txt`.
    *   Saves PDFs to the current directory.
    ```bash
    python download.py --file my_reading_list.txt
    ```

3.  **Saving to a Specific Directory**
    *   Reads URLs from `papers.md`.
    *   Saves PDFs to a folder named `downloaded_papers`.
    ```bash
    python download.py --save_dir downloaded_papers
    ```

4.  **Using a Custom Input File and Save Directory**
    *   Reads URLs from `my_reading_list.txt`.
    *   Saves PDFs to `downloaded_papers`.
    ```bash
    python download.py --file my_reading_list.txt --save_dir downloaded_papers
    ```

## How It Works

The script reads the specified input file line by line. For each URL, it checks the domain name (`arxiv.org`, `sci-hub.se`, etc.) to determine which parsing function to use. It then sends a request to the URL, parses the returned HTML using BeautifulSoup to find the direct link to the PDF, and downloads the file.

If a URL is from an unsupported website, it will print a warning and skip to the next one.

---
