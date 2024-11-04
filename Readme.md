FAKE REVIEW DETECTION USING MACHINE LEARNING
********************************************

SYSTEM REQUIREMENTS
*******************
Operating System: Windows 7 or higher
RAM: 4GB or higher

Libraries
*********
pandas(1.4.2)
scikit-learn(1.0.2)
nltk(3.7)
pickle(4.0)
numpy(1.22.3)
matplotlib(3.5.1)
textstat(0.7.3)
flask(2.1.1)

NLTK specific downloads (should work while running the project. run this if it only if project doesnt work normally)
***********************
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')

EXECUTION
*********
1.Open the command prompt and check whether all the required libraries,packages are installed in the system.

2.Navigate to the "Fake Review Detection/Source Code" directory from cmd using the cd command and press enter.

3.Now type in "python app2.py" to execute the program.

4.A development server is started which happens to be running at the address: http://127.0.0.1:5000/

5.Paste the address in the browser and click enter.

6.You'll be directed to a web page which shows the title of our project and abstract.

7.Click on login on the top right corner of the page.

8.Enter credentials username: admin & password: admin and press login to continue.

9.We see the following fields: review text, rating, verified purchase & category.

10.Now, the user can fill up the fields with the review content of his choice and press predict to view the output.

11.It can now be seen whether the review is fake or legitimate.

**************************************************************************
IF YOU ARE STILL UNABLE TO RUN THE PROJECT, REFER TO THE FAKE REVIEW DETECTION EXECUTION VIDEO TO SEE THE CMD AND HOW TO RUN.