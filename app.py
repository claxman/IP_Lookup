from flask import Flask, render_template, request
import requests as r
import socket

app = Flask(__name__)

@app.route("/")
def index():
    # ip_add = request.remote_addr
    
    ip_add = request.environ.get('HTTP_X_FORWARDED_FOR')

    return render_template("index.html", ip_add=ip_add)

@app.route("/result")
def result():
    ip = request.args.get("ip")

    proxyDict = {"http": "http://111.233.225.166:1234"}
    url = "https://tools.keycdn.com/geo.json?host="+ip
    data = r.get(url, proxies=proxyDict)
    # data = r.get(url)
    
    city = data.json()["data"]["geo"]["city"]
    
    if data.json()["data"]["geo"]["region_name"] == None:
        region = ""
    else:
        region = data.json()["data"]["geo"]["region_name"]+" ("+data.json()["data"]["geo"]["region_code"]+")"
    
    if data.json()["data"]["geo"]["postal_code"] == None:
        postalcode = ""
    else:
        postalcode = data.json()["data"]["geo"]["postal_code"]
    
    country = data.json()["data"]["geo"]["country_name"]+" ("+data.json()["data"]["geo"]["country_code"]+")"
    
    continent = data.json()["data"]["geo"]["continent_name"]+" ("+data.json()["data"]["geo"]["continent_code"]+")"
    
    coordinates = str(data.json()["data"]["geo"]["latitude"])+" (lat) / "+str(data.json()["data"]["geo"]["longitude"])+" (long)"
    
    time = data.json()["data"]["geo"]["datetime"]+" ("+data.json()["data"]["geo"]["timezone"]+")"
    
    ipaddress = data.json()["data"]["geo"]["ip"]
    
    hostname = data.json()["data"]["geo"]["host"]
    
    provider = data.json()["data"]["geo"]["isp"]
    
    asn = str(data.json()["data"]["geo"]["asn"])
    
    if region == "":
        return render_template("hostname_result.html", country=country, 
                            continent=continent, coordinates=coordinates, time=time, ipaddress=ipaddress, hostname=hostname,
                            provider=provider, asn=asn)
    else:
        return render_template("IP_result.html", city=city, region=region, postalcode=postalcode, country=country, 
                            continent=continent, coordinates=coordinates, time=time, ipaddress=ipaddress, hostname=hostname,
                            provider=provider, asn=asn)
if __name__ == "__main__":
    app.run()