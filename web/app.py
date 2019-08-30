from flask import Flask, jsonify, request
from flask_restful import Api, Resource
import os
from random import randrange as rr

path = "/usr/src/app/Api_password/"

app = Flask(__name__)
api = Api(app)



def random_generator():
    s = rr(1,9)
    return s




def encrypt(text,s): 
    result = "" 
  
    # traverse text 
    for i in range(len(text)): 
        char = text[i] 

        #Special char
        if char in ['@','#' ,'$' ,'%' , '!','&']:
            result += char
            continue
  
        # Encrypt uppercase characters 
        if (char.isupper()): 
            result += chr((ord(char) + s-65) % 26 + 65) 
  
        # Encrypt lowercase characters 
        else: 
            result += chr((ord(char) + s - 97) % 26 + 97) 
  
    return result 





def de_crypt(text,s): 
    result = "" 
  
    # traverse text 
    for i in range(len(text)): 
        char = text[i] 

        if char == '@' or char =='#' or char =='$' or char =='%' or char =='!' or char =='&':
            result += str(char)
            continue
  
        # Encrypt uppercase characters 
        if (char.isupper()): 
            result += chr((ord(char) + s-65) % 26 + 65) 
  
        # Encrypt lowercase characters 
        else: 
            result += chr((ord(char) + s - 97) % 26 + 97) 
  
    return result 






def _mkdir_():
    path1 = "/usr/src/app"
    list_dir = os.listdir(path1)
    if "Api_password" not in list_dir: 
        os.mkdir(path)
        retJson = {
            "msg" : "successfully created directory",
            "status" : 200
        }
        print(retJson)
        return True
    else:
        retJson = {
            "msg" : "directory already exist",
            "status" : 200
        }
        print(retJson)
        return True



def _mkfile_(domain,password,n):
    path1 = "/usr/src/app/Api_password"
    n = str(n)
    list_dir = os.listdir(path1)
    if  domain+".txt" not in list_dir: 
        f = open("%s/%s.txt"%(path,domain),"w+")
        f.write(password)
        f.write("\n")
        f.write(n)
        f.close()
        retJson = {
            "msg" : "successfully created %s.txt file"%domain,
            "status" : 200
        }
        print(retJson)
        return True
    else:
        retJson = {
            "msg" : "%s already exist"%domain,
            "status" : 200
        }
        print(retJson)
        return True



class encrpt_data(Resource):
    def post(self):
        postedData = request.get_json()

        domain = postedData["domain"]
        password = postedData["password"]

        n = random_generator()
        password = encrypt(password,n)

        if _mkdir_():
            if _mkfile_(domain,password,n):
                retJson = {
                "domain" : domain,
                "en_password" : password,
                "shift" : n,
                "status" : 200,
                "msg" : "Successfully created"
            }
            return jsonify(retJson)







class decrypt_data(Resource):
    def post(self):
        path1 = "/usr/src/app/Api_password"

        postedData = request.get_json()

        domain = postedData["domain"]
        
        list_file = os.listdir(path1)

        if domain+".txt" in list_file:
            file_na = list_file.index(domain+".txt")
            val = list_file[file_na]
            with open(path1+"/%s" %val, 'r') as f:
                for s in f:
                    password = s.rstrip()
                    for s in f:
                        n = s

        n = 26 - int(n)            
        password = de_crypt(password,n)

        retJson = {
            "domain" : domain,
            "decrypt_password" : password,
            "status" : 200,
            "msg" : "Successfully decrypted"
        }
        return jsonify(retJson)
                





api.add_resource(encrpt_data,'/add')
api.add_resource(decrypt_data,'/show')


if __name__ == "__main__":
    app.run(host='0.0.0.0')