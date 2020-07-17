################################ Import Packages ######################################
from flask import Flask,request
from flask_restful import Resource,Api
import os,sys,random,string,requests
import pytesseract as pt
from pytesseract import Output
import zbar
import pandas as pd
import numpy as np
from PIL import Image
############################ Create Flask App ###########################################
app=Flask(__name__)
api=Api(app)
############################ Create Helper Function ####################################
def ReadBarCode(CurrentImage):
    scanner = zbar.Scanner()
    results = scanner.scan(CurrentImage)
    barcode=""
    for result in results:
        barcode=barcode+str(result.data)
    return barcode
############################ Create Code Functionality #################################
class FetchUPC(Resource):
    def post(self):
        try:
            ################# Create Constants #####################
            DownloadDirectory="/mnt/tmp"
            randomfivedigitnumber=random.randint(10000,99999)
            letters = string.ascii_lowercase
            randomfivecharacters=''.join(random.choice(letters) for i in range(5))
            FileName="File_"+str(randomfivedigitnumber)+"_"+randomfivecharacters+".jpg"
            DownloadFilePath=DownloadDirectory+"/"+FileName
            ################# Get Request Parameters ###############
            data = request.get_json()
            file_url = data['file_url']
            ################## Download File #######################
            try:
                response=requests.get(str(file_url))
            except:
                return{'msg':'Error','description':'Unable to download file. Please check the file url again.'}
            ############# Write downloaded file to local ##########
            try:
                with open(DownloadFilePath,'wb') as f:
                    f.write(response.content)
            except:
                return{'msg':'Error','description':'Unable to save downloaded file.'}
            ################ Read Downloaded Image ################
            image = Image.open(DownloadFilePath).convert('L')
            image = np.array(image)
            ################ Check If Bar Code Exists #############
            barcode=ReadBarCode(image)
            if len(barcode)!=0:
                product_bar_code=""
                for char in barcode:
                    if char in ['0','1','2','3','4','5','6','7','8','9']:
                        product_bar_code=product_bar_code+char
                os.remove(DownloadFilePath)
                return {'msg':"Success","UPC Code":product_bar_code}
            ############# No BarCode So check UPC# ################
            else:
                image[image>185]=255
                content=pt.image_to_data(image,output_type=Output.DICT)
                os.remove(DownloadFilePath)
                res=pd.DataFrame.from_dict(content)
                res['text']=res['text'].str.lower()
                upc_code=""
                for items in res['text'].values:
                    if ('upc' in items):
                        for char in items:
                            if char in ['0','1','2','3','4','5','6','7','8','9']:
                                upc_code=upc_code+char
                        break
                if upc_code=="":
                    WholeContent=" ".join(res['text'].values)
                    WholeContentSplitted=WholeContent.split(" ")
                    for words in WholeContentSplitted:
                        if ("#" in words) and (len(words)>9):
                            for char in words:
                                if char in ['0','1','2','3','4','5','6','7','8','9']:
                                    upc_code=upc_code+char
                if upc_code=="":
                    WholeContent=" ".join(res['text'].values)
                    WholeContentSplitted=WholeContent.split(" ")
                    for words in WholeContentSplitted:
                        if len(words)>8:
                            only_number=True
                            for char in words:
                                if char not in ['0','1','2','3','4','5','6','7','8','9']:
                                    only_number=False
                                    break
                            if only_number:
                                for char in words:
                                    if char in ['0','1','2','3','4','5','6','7','8','9']:
                                        upc_code=upc_code+char
                if len(upc_code)!=0:
                    return {'msg':"Success","UPC Code":upc_code}
                else:
                    return {'msg':"Error","UPC Code":"UPC code couldn't be found."}
        except Exception as e:
            return {'msg':'Error','description':str(e)}
############################## Configure Flask Endpoint ################################
api.add_resource(FetchUPC,'/FetchUPC')
################################## Run Flask API #######################################
if __name__=='__main__':
    app.run(debug=True)
