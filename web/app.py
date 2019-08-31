from flask import Flask, jsonify, request
from flask_restful import Api, Resource
import os,stat
from random import randrange as rr

path = "/usr/src/app/Api_password/"

app = Flask(__name__)
api = Api(app)



def random_generator():
    s = rr(1,9)
    return s


def only_app(file_name):
    os.chmod("%s%s" %(path,file_name+".txt"), stat.S_IXUSR )
    return True


def only_write(file_name):
    os.chmod("%s%s"%(path,file_name+".txt"), stat.S_IWRITE )
    return True

def only_read(file_name):
    os.chmod("%s%s"%(path,file_name+".txt"), stat.S_IRUSR )
    return True


def rename(file_name):
    os.chdir("/usr/src/app/Api_password/")
    os.rename(file_name+".txt",file_name+".dng")   
    return True

def rename_dng(file_name):
    os.chdir("/usr/src/app/Api_password/")
    os.rename(file_name+".dng",file_name+".txt")
    return True




def encrypt(text,s): 
    result = "" 
  
    # traverse text 
    for i in range(len(text)): 
        char = text[i]

        if (char.isnumeric()):
            result += char
            continue 

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

        if (char.isnumeric()):
            result += char
            continue



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
    path1 = "/usr/src/app/"
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



def _mkfile_(file_name,password,n):
    path1 = "/usr/src/app/Api_password"
    n = str(n)
    list_dir = os.listdir(path1)
    if  file_name+".txt" not in list_dir: 
        f = open("%s/%s.txt"%(path,file_name),"w+")
        f.write(password)
        f.write("\n")
        f.write(n)
        f.close()
        only_write(file_name)
        retJson = {
        "msg" : "successfully created %s.txt file"%file_name,
        "status" : 200
        }
        only_app(file_name)
        print(retJson)
        if rename(file_name):
            return True
    else:
        if rename_dng(file_name):
            only_write(file_name)
            f = open("%s%s.txt"%(path,file_name),"w")
            f.write(password)
            f.write("\n")
            f.write(n)
            f.close()
            retJson = {
                "msg" : "%s already exist"%file_name,
                "status" : 200
            }
            only_app(file_name)
            print(retJson)
        if rename(file_name):
            return True



class encrpt_data(Resource):
    def post(self):
        postedData = request.get_json()

        file_name = postedData["file_name"]
        password = postedData["password"]

        n = random_generator()
        password1 = encrypt(password,n)

        if _mkdir_():
            if _mkfile_(file_name,password1,n):
                retJson = {
                "domain" : file_name,
                "your_password" : password,
                "en_password" : password1,
                "shift" : n,
                "status" : 200,
                "msg" : "Successfully created"
            }
            return jsonify(retJson)







class decrypt_data(Resource):
    def post(self):
        path1 = "/usr/src/app/Api_password"

        postedData = request.get_json()

        file_name = postedData["file_name"]

        rename_dng(file_name)
        
        if only_read(file_name):
        
            list_file = os.listdir(path1)

            if file_name+".txt" in list_file:
                file_na = list_file.index(file_name+".txt")
                val = list_file[file_na]
                with open(path1+"/%s" %val, 'r') as f:
                    for s in f:
                        password = s.rstrip()
                        for s in f:
                            n = s
        if only_app(file_name):

            rename(file_name)

            n = 26 - int(n)            
            password = de_crypt(password,n)

            retJson = {
                "filename" : file_name,
                "decrypt_password" : password,
                "status" : 200,
                "msg" : "Successfully decrypted"
            }
            return jsonify(retJson)
                





api.add_resource(encrpt_data,'/add')
api.add_resource(decrypt_data,'/show')


if __name__ == "__main__":
    app.run(host='0.0.0.0')
