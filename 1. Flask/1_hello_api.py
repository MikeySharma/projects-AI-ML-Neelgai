from flask import Flask

app=Flask(__name__)

@app.route('/')
def home():
    return "Hello world"

@app.route('/new')
def new_home():
    return "Hello new worldssssdadadaaddddddddddddddadad"

        
if __name__=='__main__':
    app.run(host='0.0.0.0',port=5050,debug=True)