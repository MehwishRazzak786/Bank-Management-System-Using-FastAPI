# Bank Management System

This project is a simple bank management system with a backend API built using FastAPI and a web-based user interface created with Streamlit.

## Features

*   User authentication based on username and PIN.
*   Deposit funds into a user's account.
*   Transfer funds between users.

## Technologies Used

*   **Backend:** Python, FastAPI
*   **Frontend:** Python, Streamlit
*   **API Interaction:** `requests` library

## Getting Started

### Prerequisites

*   Python 3.x
*   pip

### Installation

1.  Clone the repository:
    ```bash
    git clone <https://github.com/MehwishRazzak786/Bank-Management-System-Using-FastAPI.git>
    ```
2.  Navigate to the project directory:
    ```bash
    cd fast-API-project
    ```
3.  Install the required dependencies:
    ```bash
    pip install fastapi uvicorn streamlit requests
    ```

### Running the Application

1.  **Start the FastAPI Backend:**
    Open your terminal or command prompt and run the following command:
    ```bash
    uv run uvicorn main:app --reload
    ```
    The backend API will be running at `http://127.0.0.1:8000`.

2.  **Start the Streamlit Frontend:**
    Open a *new* terminal or command prompt and run the following command:
    ```bash
    streamlit run ui.py
    ```
    The Streamlit UI will be accessible in your web browser at `http://localhost:8501`.

## Usage

The application provides a user-friendly interface to interact with the bank API.

### Test Users

You can use the following pre-configured users to test the application:

| Username | PIN    | Balance |
|----------|--------|---------|
| mehwish  | 7777   | 10000   |
| Aabis    | 6666   | 7000    |
| Adeeba   | 5555   | 15000   |

1.  **Authentication:** Enter a username and PIN in the "User Authentication" section and click "Authenticate".
2.  **Deposit:** Once authenticated, you can deposit funds into your account using the "Deposit Funds" section.
3.  **Bank Transfer:** You can transfer funds to another user using the "Bank Transfer" section.

## API Endpoints

The FastAPI backend provides the following endpoints:

*   `POST /authenticate`: Authenticates a user.
    *   **Query Parameters:** `name` (string), `pin_number` (integer)
*   `POST /deposit`: Deposits funds into a user's account.
    *   **Query Parameters:** `name` (string), `amount` (float)
*   `POST /bank-transfer`: Transfers funds between users.
    *   **Query Parameters:** `sender_name` (string), `sender_pin` (integer), `recipient_name` (string), `amount` (float)
*   `GET /`: Root endpoint to check if the API is running.