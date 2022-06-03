from flask import Flask,render_template,request
import requests

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "AQvqQUy6eelddWBUYhkNQPVXS7VHPXRoQVTPKKGrdwmi"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
 API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}
#import pickle
app=Flask(__name__)
#model=pickle.load(open('Car.pkl','rb'))

@app.route('/')
def hello():
    return render_template("carp.html")

@app.route('/login',methods=['POST'])
def User():
    a=request.form["cycle"]
    b=request.form["disp"]
    c=request.form["hp"]
    d=request.form["wt"]
    e=request.form["acc"]
    f=request.form["my"]
    s=request.form["s"]
    
    t=[[int(a),int(b),int(c),int(d),int(e),int(f),int(s)]]
    #y=model.predict(t)
    # NOTE: manually define and pass the array(s) of values to be scored in the next line
    payload_scoring = {"input_data": [{"fields": ["f0","f1","f2","f3","f4","f5","f6"], "values": t}]}

    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/7fa14f91-d730-4c7e-90a9-8c9c17f5a001/predictions?version=2022-06-02', json=payload_scoring,
    headers={'Authorization': 'Bearer ' + mltoken})
    print("Scoring response")
    #print(response_scoring.json())
    pred=response_scoring.json();
    out=pred['predictions'][0]['values'][0][0]
    print(out)
    
    return render_template("carp.html",y="The Mileage per Gallon would be "+str(out))

if __name__=='__main__':
    app.run(debug=False)