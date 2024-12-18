from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add', methods=['POST'])
def add_numbers():
    
    first_num = int(request.form['first_num'])
    second_num = int(request.form['second_num'])
    sum_result = first_num + second_num

    return render_template('result.html', first_num=first_num, second_num=second_num, sum_result=sum_result)

if __name__ == '__main__':
    app.run(debug=True)
