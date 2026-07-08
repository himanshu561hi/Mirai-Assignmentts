# The Identity Echo Interface

A simple and interactive **Streamlit** application developed as part of the **MirAI School of Technology – Virtual Summer Internship 2026 (AI Builder Track)**.

The application collects a user's **Name** and **Message**, validates the input, and displays a personalized response. It also includes an estimated **AI token usage calculator**, demonstrating the relationship between message length and token consumption.

---

## Features

- Interactive Streamlit user interface
- Collects user's name and message
- Input validation for empty fields
- Personalized success message
- Estimates AI token usage based on message length
- Displays character count and estimated token count
- Beginner-friendly and responsive design

---

## 🛠️ Tech Stack

- Python 3.x
- Streamlit

---

## Project Structure

```
The Identity Echo Interface/
│── app.py
│── requirements.txt
└── README.md
```

---

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
```

### 2. Navigate to the Project Directory

```bash
cd "The Identity Echo Interface"
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

or

```bash
python3 -m pip install -r requirements.txt
```

---

## Run the Application

```bash
python3 -m streamlit run app.py
```

After running the command, Streamlit will generate a local URL similar to:

```
http://localhost:8501
```

Open the URL in your browser to access the application.

---

## How to Use

1. Enter your **Name**.
2. Enter a **Message**.
3. Click the **Transmit** button.
4. The application validates the inputs:
   - Displays an error if the name is missing.
   - Displays a warning if the message is missing.
   - Displays a success message when both fields are provided.
5. View the estimated AI token consumption for your message.

---

## Token Cost Estimator

The application includes a simple token estimation feature based on the common approximation:

```
1 Token ≈ 4 Characters
```

For every submitted message, the application calculates:

- Total characters
- Estimated token count
- Displays the result using Streamlit's information component

---

## Application Features

- Modern Streamlit interface
- Name input field
- Message input field
- Transmit button
- Error handling
- Warning messages
- Success confirmation
- Token usage estimation
- Character statistics

---

## Requirements

- Python 3.8 or above
- Streamlit

Install dependencies using:

```bash
pip install -r requirements.txt
```

---

## Assignment Details

**Internship:** MiraI School of Technology

**Program:** Virtual Summer Internship 2026 – AI Builder Track

**Assignment:** The Identity Echo Interface

---

## Author

**Himanshu Gupta**

Developed as part of the **MirAI School of Technology Virtual Summer Internship 2026**.

---

## License

This project is created for educational purposes as part of the **MirAI School of Technology Internship Assignment**.
