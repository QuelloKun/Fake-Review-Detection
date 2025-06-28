# Fake Review Detection Using Machine Learning

-----

## System Requirements

  * **Operating System:** Windows 7 or higher
  * **RAM:** 4GB or higher

-----

## Libraries

The following Python libraries are required:

  * **pandas:** 1.4.2
  * **scikit-learn:** 1.0.2
  * **nltk:** 3.7
  * **pickle:** 4.0
  * **numpy:** 1.22.3
  * **matplotlib:** 3.5.1
  * **textstat:** 0.7.3
  * **flask:** 2.1.1

-----

## NLTK Downloads

If the project doesn't run normally, you might need to manually download these NLTK components:

```python
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')
```

-----

## Execution Guide

Follow these steps to run the fake review detection system:

1.  **Verify Libraries:** Open your command prompt and confirm that all the required libraries and packages listed above are installed on your system.
2.  **Navigate to Source Code:** Use the `cd` command in your command prompt to navigate to the "Fake Review Detection/Source Code" directory.
    ```bash
    cd "Fake Review Detection/Source Code"
    ```
3.  **Execute the Program:** Type the following command and press Enter to start the program:
    ```bash
    python app2.py
    ```
4.  **Access the Web Application:** A development server will start, typically running at: `http://127.0.0.1:5000/`
5.  **Open in Browser:** Paste this address into your web browser and press Enter. You'll be directed to a web page displaying the project title and abstract.
6.  **Login:** Click on the "Login" link located in the top-right corner of the page.
7.  **Enter Credentials:** Use the following credentials to log in:
      * **Username:** `admin`
      * **Password:** `admin`
    <!-- end list -->
8.  **Input Review Details:** After logging in, you'll see fields for "review text," "rating," "verified purchase," and "category."
9.  **Predict:** Fill in the fields with your desired review content and click the "Predict" button to view the output.
10. **View Results:** The system will then indicate whether the entered review is fake or legitimate.
