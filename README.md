# Precise Extract

Precise Extract is a web application that enables users to input their structured data (tabular data) in bulk from PDF or image formats, extract the data, and store it in an SQL database. Users can run natural language queries on this data and extract the results in Excel format.

## Table of Contents

- [Features](#features)
- [Technical Details](#technical-details)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Features

- Extract tabular data from PDF, JPEG, PNG, and JPG files.
- Bulk upload with consistent schema.
- Store extracted data in an SQL database.
- Run natural language queries on the data.
- Export queried data and entire tables to Excel format.
- User authentication and session management.

## Technical Details

### Frontend
- **Technologies:** HTML, CSS, JavaScript

### Backend
- **Technologies:** Flask, FastAPI
- **Database:** MySQL
- **Data Extraction:** PaddleOCR from Baidu's PaddlePaddle
- **Natural Language to SQL:** Gemini API or ChatGPT

### Workflow
1. **User Interaction:** Users sign up, log in, and upload files.
2. **Data Upload:** Files are uploaded to the FastAPI server with JWT and AES encryption for authentication.
3. **Data Extraction:** PDFs are converted to images, and tabular data is extracted using PaddleOCR.
4. **Data Storage:** Extracted data is stored in a shared SQL database.
5. **Querying:** Users can run natural language queries, processed by Gemini or ChatGPT, to get SQL queries executed on the data.
6. **Data Export:** Users can export tables or query results to Excel format.

## Installation

1. **Clone the Repository:**
    ```bash
    git clone https://github.com/your-repo/precise-extract.git
    cd precise-extract
    ```

2. **Database Setup:**
    - Import the `precise_extract.sql` file into your local SQL database.

3. **Install Requirements:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Run the Servers:**
    - **Flask Server:**
      ```bash
      cd backend
      python run.py
      ```
    - **FastAPI Server:**
      ```bash
      cd fastapi
      uvicorn myapp:app --host 0.0.0.0 --reload
      ```

5. **Configuration:**
    - Update the IP address in `myapp.py` (FastAPI folder) and in `main(4).html` and `home4.html` (Frontend files) with your PC's IP address and the respective ports (5000 for Flask, 8000 for FastAPI).

## Usage

1. **Access the Website:**
    - Open your browser and navigate to the IP address of your Flask server (e.g., `http://your-ip-address:5000`).

2. **Sign Up / Log In:**
    - Create an account or log in to start using the service.

3. **Upload Files:**
    - Use the input section to browse or drag and drop files. Ensure files have the same schema for bulk uploads.

4. **Data Extraction:**
    - After uploading, the system will process the files and display the extracted data headers for confirmation.

5. **Run Queries:**
    - Use the provided text box to enter natural language queries. The results will be displayed on the screen.

6. **Export Data:**
    - Use the export options to download data in Excel format.

## Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a new Pull Request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

For any questions or issues, please open an issue in the repository or contact the maintainers.

Happy extracting!
