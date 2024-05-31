# Flask Audio Transcription Application

This Flask application provides a platform for teachers to transcribe their speech in real-time. The transcriptions can be viewed by students on a separate page and downloaded as a PDF. The application also supports user registration and login for both students and instructors.

## Features

- Real-time audio transcription
- User registration and login
- Separate interfaces for teachers and students
- Download transcriptions as PDF

## Table of Contents

- [Installation](#installation)
- [Setup](#setup)
- [Running the Application](#running-the-application)
- [Usage](#usage)
- [Files](#files)

## Installation

### Prerequisites

Ensure you have the following installed:

- Python 3.9.10 
- pip
- wkhtmltopdf

### Clone the Repository

```sh
git clone https://github.com/MGASALUCAS/trans_api.git
cd trans_api
```

### Install Dependencies

```
 pip install Flask Flask-SocketIO pdfkit flask_login
```

### Running the app.

```
python main.py

```

### Usage
#### Teacher's Page
-   Navigate to http://localhost:5000/instructor
-   Register or log in as an instructor
-   Start speaking and see real-time transcriptions

#### Student's Page
-   Navigate to http://localhost:5000/student
-   View real-time transcriptions
-   Click the download button to save the transcription as a PDF

