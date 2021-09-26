from flask import * 
import requests
from xml.etree import ElementTree as et

app = Flask(__name__) #creating the Flask class object   

API_KEY = ''
address = "# 3582,13 G Main Road, Indiranagar,Bengaluru, Karnataka 560008"
 
@app.route('/') #decorator drfines the  
def home():  
    return render_template('home.html')

@app.route('/getAddressDetails',methods = ['POST','GET'])
def results():
    if(request.method == 'POST'): 
        result = request.form
        address=result['address']
        output_format=result['output_format']
        params = {
            'key':API_KEY,
            'address':address
        }
        base_url = 'https://maps.googleapis.com/maps/api/geocode/json'
        response = requests.get(base_url,params=params).json()
        if(response['status']=='OK'):
                geometry = response['results'][0]['geometry']
                lat = geometry['location']['lat']
                long = geometry['location']['lat']
        else:
            res_obj = {"error":"something went wrong"}
            return render_template('home.html',response=res_obj)
        if(output_format=='json'):
            res_obj = {"coordinates":{"lat":lat,"long":long},"address":address}
            res_obj=json.dumps(res_obj)
            return render_template('home.html',response=res_obj)
        else:
            res_obj = """
            <?xml version="1.0" encoding="UTF-8"?>
            <root>
            <address>{0}</address>
            <coordinates>
            <lat>{1}</lat>
            <lng>{2}</lng>
            </coordinates>
            </root>
            """
            res_obj = res_obj.format(address,lat,long)
            return render_template('home.html',response=res_obj)
    else:
        return render_template('home.html')
  
if __name__ =='__main__':  
    app.run(debug = True)  