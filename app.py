from flask import Flask, request, render_template, redirect
import requests, json
import ast

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def home():
    worth = []
    names = []
    industries = []
    defaultLimit = 10
    #response = requests.get(f"https://forbes400.herokuapp.com/api/forbes400?limit={defaultLimit}")
    if request.method == 'POST':
        limit = request.form.get('limitRange', defaultLimit)
        response = requests.get(f"https://forbes400.herokuapp.com/api/forbes400?limit={int(limit)}")
        for i in response.json():
            worth.append(i['finalWorth'])
            names.append(i['personName'])
            industries.append(i['industries']) 
        return render_template('home.html',names=names, worth=worth, industries=industries)
    else:    
        response = requests.get(f"https://forbes400.herokuapp.com/api/forbes400?limit={defaultLimit}")   
        for i in response.json():
            worth.append(i['finalWorth'] / 1000)
            names.append(i['personName'])
            industries.append(i['industries'])
        return render_template('home.html',names=names, worth=worth, industries=industries)


@app.route("/lookUp/<pg_no>", methods=['GET'])
def lookUp_page(pg_no):
    response = requests.get('https://forbes400.herokuapp.com/api/forbes400')
    info_list = []
    if int(pg_no) == 1:
        start = 0
    else:    
        start = int(pg_no) * 100 - 100
    for i in response.json():
        if int(i['rank']) > start and int(i['rank']) <= (int(pg_no) * 100):
            info_list.append(i)
    return render_template('Look_up.html', info_list=info_list) 


@app.route("/lookUp/person/<name>", methods=['GET'])
def lookUpPerson(name):
    print(name)
    names = []
    n_shares = []
    fn_assets = []
    response = requests.get('https://forbes400.herokuapp.com/api/forbes400')
    for i in response.json():
        if i['personName'] == name:
            rank = i['rank']
            if 'state' in i:
                state = i['state']
            else:
                state = ""  
            if "city" in i:
                city = i['city']
            else:
                city = ""
            if "financialAssets" in i:
                for n in i['financialAssets']:
                    names.append(n['companyName'])
                    n_shares.append(n['numberOfShares'] / 1000)
                fn_assets.append(i['financialAssets'])
            else:
                fn_assets = []
            if "finalWorth" in i:
                netWorth = i['finalWorth']
            else:
                netWorth = ""
            if "squareImage" in i:
                image = i['squareImage']
            else:
                image = ""
            if "bios" in i:        
                bios = i['bios']
            else:
                bios = ""
            if "abouts" in i:    
                abouts = i['abouts']
            else:
                abouts = ""    
    return render_template('person.html', name=name, rank=rank, state=state, city=city, fn_assets=fn_assets, netWorth=netWorth, image=image, bios=bios, abouts=abouts, names=names, n_shares=n_shares)        

@app.route('/about', methods=['GET'])
def aboutPage():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(threaded=True, port=5000)