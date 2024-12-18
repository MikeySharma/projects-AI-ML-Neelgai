from flask import Flask,request

app=Flask(__name__)

@app.route('/')
def home():
    return "Hello World"

@app.route('/get/<user>')
def name(user):
    return 'Hello ' + user

@app.route('/json/',methods=['POST'])
def json_example():
    info={}
    
    data=request.get_json()

    a=data['first_num']
    b=data['second_num']
    
    sum=a+b
    
    info['input']=[a,b]
    info['sum']=sum
    
    '''return jsonify({
        "input":info,
        "sum":sum
        })'''
    return info


if __name__=='__main__':
    app.run(host='0.0.0.0',port=5050,debug=True)