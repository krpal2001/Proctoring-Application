import subprocess
from flask import Flask, redirect
from flask import Flask, render_template, render_template, session, redirect, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def run_streamlit():
    try:
        # Start Streamlit in a new background process
        # This subprocess will continue to run after Flask app is closed
        subprocess.Popen(["streamlit", "run", "main.py"])
        # return redirect("http://localhost:8501")
    except Exception as e:
        return str(e)

@app.route('/monitor.py')
def open_module1():
    # Your code to run module1.py
    try:
        # Run module1.py script located in the same directory as this Flask app
        subprocess.run(['python', 'monitor.py'], check=True)
        return '''
        <html>
            <head>
                <title>Module Execution</title>
            </head>
            <body style="background-image: url('https://odmps.org/updates/wp-content/uploads/2022/02/students-knowing-right-answer_329181-14271-1.webp'); background-size: cover;">
            </body>
        </html>
        '''
        # return 'Module 1 has been executed successfully!'
    except subprocess.CalledProcessError:
        return 'An error occurred while executing Module 1.'

@app.route('/proctoring.py')
def open_module2():
    # Your code to run module2.py
    try:
        # Run module1.py script located in the same directory as this Flask app
        subprocess.run(['python', 'proctoring.py'], check=True)
        return 'Module 2 has been executed successfully!'
        # return '''
        # <html>
        #     <head>
        #         <title>Module Execution</title>
        #     </head>
        #     <body style="background-image: url('https://s3.amazonaws.com/prod-hmhco-vmg-craftcms-public/highschool-classroom-management-hero.jpg'); background-size: cover;">
        #     </body>
        # </html>
        # '''
    except subprocess.CalledProcessError:
        return 'An error occurred while executing Module 2.'

@app.route('/main.py')
def open_module3():
    # Your code to run module3.py
    run_streamlit()
    # return redirect("http://localhost:8501")
    return redirect('http://127.0.0.1:5000')



if __name__ == '__main__':
    app.run(debug=True)
