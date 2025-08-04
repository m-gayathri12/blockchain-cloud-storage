from django.shortcuts import render
from django.template import RequestContext
from django.contrib import messages
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
import numpy as np
import base64
import os
from datetime import date
from hashlib import sha256
import Convergent
import json
from web3 import Web3, HTTPProvider
import matplotlib.pyplot as plt
import timeit
import io
import pandas as pd
import pickle
import ipfsapi
import sys
import urllib, mimetypes

api = ipfsapi.Client(host='http://127.0.0.1', port=5001)

global username, usersList, metadataList
global contract, web3
computation_time = []
storage_size = []

#function to call contract
def getContract():
    global contract, web3
    blockchain_address = 'http://127.0.0.1:9545'
    web3 = Web3(HTTPProvider(blockchain_address))
    web3.eth.defaultAccount = web3.eth.accounts[0]
    compiled_contract_path = 'Deduplicate.json' #Deduplicate contract file
    deployed_contract_address = '0x78A66B9Dae16409dd0C426175cD3d0b84F696337' #contract address
    with open(compiled_contract_path) as file:
        contract_json = json.load(file)  # load contract info as JSON
        contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
    file.close()
    contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)
getContract()

def getUsersList():
    global usersList, contract
    usersList = []
    count = contract.functions.getUserCount().call()
    for i in range(0, count):
        user = contract.functions.getUsername(i).call()
        password = contract.functions.getPassword(i).call()
        phone = contract.functions.getPhone(i).call()
        email = contract.functions.getEmail(i).call()
        address = contract.functions.getAddress(i).call()
        usersList.append([user, password, phone, email, address])

def getMetadataList():
    global metadataList, contract
    metadataList = []
    count = contract.functions.getMetadataCount()().call()
    for i in range(0, count):
        owner = contract.functions.getOwner(i).call()
        filename = contract.functions.getFilename(i).call()
        block_no = contract.functions.getBlockNo(i).call()
        hashcode = contract.functions.getBlockhash(i).call()
        upload_date = contract.functions.getUploadDate(i).call()
        metadataList.append([owner, filename, block_no, hashcode, upload_date])

getUsersList()
getMetadataList()

def Graph(request):
    if request.method == 'GET':
        global storage_size, computation_time
        index = []
        for i in range(len(computation_time)):
            index.append(i+1)
        existing = 0
        propose = 0
        for i in range(len(storage_size)):
            size = storage_size[i]
            propose = propose + size[1]
            existing = existing + size[0]
        figure, axis = plt.subplots(nrows=1, ncols=2,figsize=(10,4))
        axis[0].set_title("Storage Graph")
        axis[1].set_title("Computation Time Graph")
        axis[1].plot(index, computation_time, label="Computation Time")
        axis[1].legend()
        '''
        axis[0].bar(existing, propose)
        axis[0].set_xlabel("Technique Name")
        axis[0].set_ylabel("Storage Size")
        plt.xticks([1, 2], ['Existing', 'Propose', rotation=45)
        '''
        df = pd.DataFrame([[existing, propose]], columns=['Existing', 'Propose'])
        df.plot(ax=axis[0], kind='bar')
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight')
        plt.close()
        img_b64 = base64.b64encode(buf.getvalue()).decode()    
        context= {'data':'Comparison Graph', 'img': img_b64}
        return render(request, 'UserScreen.html', context)       

def DownloadAction(request):
    if request.method == 'GET':
        global username, metadataList
        filename = request.GET['file']
        for i in range(len(metadataList)):
            ml = metadataList[i]
            if ml[1] == filename:
                codes = ml[3].split(" ")
                if os.path.exists("DeduplicateApp/static/"+filename):
                    os.remove("DeduplicateApp/static/"+filename)
                with open("DeduplicateApp/static/"+filename, "wb+") as myfile:
                    for k in range(len(codes)):
                        arr = codes[k].split("$")
                        content = api.get_pyobj(arr[0])
                        content = pickle.loads(content)
                        content = Convergent.decrypt(content)
                        myfile.write(content)
                myfile.close()
                break
        with open("DeduplicateApp/static/"+filename, "rb") as myfile:
            data = myfile.read()
        myfile.close()
        response = HttpResponse(data,content_type='application/force-download')
        response['Content-Disposition'] = 'attachment; filename='+filename
        return response    

def Download(request):
    if request.method == 'GET':
        global username, metadataList
        output = '<table border=1 align=center>'
        output+='<tr><th><font size=3 color=black>Uploader Name</font></th>'
        output+='<th><font size=3 color=black>Filename</font></th>'
        output+='<th><font size=3 color=black>Uploading Date</font></th>'
        output+='<th><font size=3 color=black>Download File</font></th></tr>'
        dups = []
        for i in range(len(metadataList)):
            arr = metadataList[i]
            if arr[0] == username:
                if arr[1] not in dups:
                    dups.append(arr[1])
                    output+='<tr><td><font size=3 color=black>'+arr[0]+'</font></td>'
                    output+='<td><font size=3 color=black>'+arr[1]+'</font></td>'
                    output+='<td><font size=3 color=black>'+arr[4]+'</font></td>'
                    output+='<td><a href=\'DownloadAction?file='+arr[1]+'\'><font size=3 color=black>Click Here</font></a></td></tr>'
        context= {'data': output}        
        return render(request, 'UserScreen.html', context)

def ViewBlocks(request):
    if request.method == 'GET':
        global username,metadataList
        output = '<table border=1 align=center>'
        output+='<tr><th><font size=3 color=black>Uploader Name</font></th>'
        output+='<th><font size=3 color=black>Filename</font></th>'
        output+='<th><font size=3 color=black>Block No</font></th>'
        output+='<th><font size=3 color=black>Block Hashcode</font></th>'
        output+='<th><font size=3 color=black>Upload Date</font></th></tr>'
        dups = []
        for i in range(len(metadataList)):
            ml = metadataList[i]
            blocks = ml[2].split(" ")
            codes = ml[3].split(" ")
            if ml[1] not in dups:
                dups.append(ml[1])
                for k in range(len(blocks)):
                    arr = codes[k].split("$")
                    if ml[0] == username:
                        output+='<tr><td><font size=3 color=black>'+ml[0]+'</font></td>'
                        output+='<td><font size=3 color=black>'+ml[1]+'</font></td>'
                        output+='<td><font size=3 color=black>'+blocks[k]+'</font></td>'
                        output+='<td><font size=3 color=black>'+arr[1]+'</font></td>'
                        output+='<td><font size=3 color=black>'+ml[4]+'</font></td></tr>'
        context= {'data': output}        
        return render(request, 'UserScreen.html', context)     

def rampSecret(file_data):
    length = len(file_data)
    tot_blocks = 0
    size = 0
    if length >= 1000:
        size = length / 10
        tot_blocks = 10
    if length < 1000 and length > 500:
        size = length / 5
        tot_blocks = 5
    if length < 500 and length > 1:
        size = length / 3
        tot_blocks = 3
    return int(size), tot_blocks, length

def checkDuplicate(file_hash):
    global metadataList
    status = '<font size="3" color="blue">No Duplicate</font>'
    for i in range(len(metadataList)):
        ml = metadataList[i]
        arr = ml[3].split(" ")
        for k in range(len(arr)):
            codes = arr[k].split("$")[1]
            if codes == file_hash:
                status = '<font size="3" color="red">Duplicate Found</font>'
                break
    return status   

def UploadAction(request):
    if request.method == 'POST':
        global username, metadataList, computation_time, storage_size
        today = date.today()   
        filedata = request.FILES['t1'].read()
        filename = request.FILES['t1'].name
        size, tot_blocks, length = rampSecret(filedata)
        names = ""
        code = ""
        start = 0
        end = size
        dup_status = []
        start_time = timeit.default_timer()
        for i in range(0, tot_blocks):
            print(str(start)+" "+str(end))
            chunk = filedata[start:end]
            chunk, file_hash = Convergent.encrypt(chunk)
            start = end
            end = end + size
            chunk = pickle.dumps(chunk)
            hashcode = api.add_pyobj(chunk)
            names += filename+"_block_"+str(i)+" "
            code += hashcode+"$"+file_hash+" "
            status = checkDuplicate(file_hash)
            dup_status.append(status)
            if 'No' in status:
                sizes = sys.getsizeof(chunk)
                storage_size.append([sizes, sizes])
            else:
                sizes = sys.getsizeof(chunk)
                storage_size.append([sizes, 0])
        remain =  length - start
        if remain > 0:
            chunk = filedata[start:length]
            chunk, file_hash = Convergent.encrypt(chunk)
            start = start + remain
            chunk = pickle.dumps(chunk)
            hashcode = api.add_pyobj(chunk)
            names += filename+"_block_"+str(len(dup_status)+1)+" "
            code += hashcode+"$"+file_hash+" "
            status = checkDuplicate(file_hash)
            dup_status.append(status)
            if 'No' in status:
                sizes = sys.getsizeof(chunk)
                storage_size.append([sizes, sizes])
            else:
                sizes = sys.getsizeof(chunk)
                storage_size.append([sizes, 0])
        names = names.strip()
        code = code.strip()
        code_arr = code.split(" ")
        names_arr = names.split(" ")
        upload_date = str(date.today())   
        msg = contract.functions.saveMetadata(username, filename, names, code, upload_date).transact()
        tx_receipt = web3.eth.waitForTransactionReceipt(msg)
        metadataList.append([username, filename, names, code, upload_date])
        end = timeit.default_timer()
        computation_time.append((end - start_time))
        output = '<table border=1 align=center>'
        output+='<tr><th><font size=3 color=black>Uploader Name</font></th>'
        output+='<th><font size=3 color=black>Filename</font></th>'
        output+='<th><font size=3 color=black>Uploading Date</font></th>'
        output+='<th><font size=3 color=black>Chunk Name</font></th>'
        output+='<th><font size=3 color=black>Duplicate Status</font></th>'
        output+='<th><font size=3 color=black>Chunk Hashcode</font></th></tr>'
        for i in range(len(dup_status)):
            hashing_code = code_arr[i].split("$")
            output+='<tr><td><font size=3 color=black>'+username+'</font></td>'
            output+='<td><font size=3 color=black>'+filename+'</font></td>'
            output+='<td><font size=3 color=black>'+upload_date+'</font></td>'
            output+='<td><font size=3 color=black>'+names_arr[i]+'</font></td>'
            output+='<td><font size=3 color=black>'+dup_status[i]+'</font></td>'
            output+='<td><font size=3 color=black>'+hashing_code[1]+'</font></td></tr>'
        context= {'data': output}
        return render(request, 'UserScreen.html', context)

def Upload(request):
    if request.method == 'GET':
        return render(request, 'Upload.html', {})

def Login(request):
    if request.method == 'GET':
        return render(request, 'Login.html', {})

def index(request):
    if request.method == 'GET':
        return render(request, 'index.html', {})

def Register(request):
    if request.method == 'GET':
       return render(request, 'Register.html', {})

def Signup(request):
    if request.method == 'POST':
        global usersList
        username = request.POST.get('username', False)
        password = request.POST.get('password', False)
        contact = request.POST.get('contact', False)
        email = request.POST.get('email', False)
        address = request.POST.get('address', False)
        count = contract.functions.getUserCount().call()
        status = "none"
        for i in range(0, count):
            user1 = contract.functions.getUsername(i).call()
            if username == user1:
                status = "exists"
                break
        if status == "none":
            msg = contract.functions.saveUser(username, password, contact, email, address).transact()
            tx_receipt = web3.eth.waitForTransactionReceipt(msg)
            usersList.append([username, password, contact, email, address])
            context= {'data':'<font size="3" color="blue">Signup Process Completed</font><br/>'+str(tx_receipt)}       
            return render(request, 'Register.html', context)
        else:
            context= {'data':'Given username already exists'}
            return render(request, 'Register.html', context)

def UserLogin(request):
    if request.method == 'POST':
        global username, contract, usersList
        username = request.POST.get('username', False)
        password = request.POST.get('password', False)
        status = 'none'
        for i in range(len(usersList)):
            ulist = usersList[i]
            user1 = ulist[0]
            pass1 = ulist[1]            
            if user1 == username and pass1 == password:
                status = "success"
                break
        if status == 'success':
            output = '<font size="3" color="blue">Welcome '+username+'</font>'
            context= {'data':output}
            return render(request, "UserScreen.html", context)
        if status == 'none':
            context= {'data':'Invalid login details'}
            return render(request, 'Login.html', context)

