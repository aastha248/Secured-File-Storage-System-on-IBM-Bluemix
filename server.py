import os
import pyDes
import swiftclient
import string
import ctypes
from flask import Flask, request, make_response, redirect, url_for, send_from_directory

app = Flask(__name__)

auth_url = "https://identity.open.softlayer.com/v3"
password = "Mzj.c_*2)XYF1,&u"
project_id = "1d8b3deb5ae54027975c1ac53d5e8227"
user_id = "58573a9756f34676b1ef097043036915"
region_name = "dallas"

conn = swiftclient.Connection(key=password, authurl=auth_url, auth_version='3',
                              os_options={"project_id": project_id, "user_id": user_id, "region_name": region_name})

cont_name = "original_files"
conn.put_container(cont_name)

cont_name = "backup_files"
conn.put_container(cont_name)

FILE_ATTRIBUTE_HIDDEN = 0x02

if not os.path.isfile("keys.txt") :
  fil = open("keys.txt", 'a')
ret = ctypes.windll.kernel32.SetFileAttributesW(ur'C://Users//Aastha//Documents//Quiz1_aastha_5289//keys.txt', FILE_ATTRIBUTE_HIDDEN)

def key_processing(key) :
  if len(key) > 8:
    key = key[:8]
  elif len(key) < 8:
    key = key.rjust(8, '0')
  return key

@app.route('/uploads', methods=['GET', 'POST'])
def upload_file():
  file_contents = ""
  file_name = ""
  key = ""
  if request.method == 'POST':
    curr_file = request.files['file_upload']
    key = request.form['key']
  file_name = curr_file.filename
  file_contents = curr_file.read()
  for data in conn.get_container("original_files")[1]:
      if str(data['name']) == file_name :
        obj_tuple = conn.get_object("original_files", file_name)
        with open("keys.txt", "r") as info:
          information = info.read()
        information = information.split(";")
        for data in information :
          if (file_name in data) & ("original_files" in data) :
            data = data.split(" ")
            temp_key = key_processing(data[2])
            k = pyDes.des(bytes(temp_key), pyDes.CBC, b"\0\0\0\0\0\0\0\0", pad=None, padmode=pyDes.PAD_PKCS5)
            file_data = k.decrypt(obj_tuple[1])
        if file_contents == file_data :
          return "File Exists"
        else:
          conn.put_object("backup_files", file_name, contents=obj_tuple[1], content_type="plain/text")
          conn.delete_object("original_files", file_name)
          with open("keys.txt", "r") as info:
            information = info.read()
          information = information.split(";")
          with open("keys.txt", "w") as keyfile:
            keyfile.write("")
          with open("keys.txt", "a") as keyfile:
            for data in information:
              if (file_name in data) & ("original_files" in data):
                data = string.replace(data, "original_files", "backup_files")
              if len(data) > 5 :
                keyfile.write(data + " ;")
  with open("keys.txt", "a") as keyfile:
    keyfile.write(file_name + " original_files " + key + " ;")
  key = key_processing(key)
  k = pyDes.des(bytes(key), pyDes.CBC, b"\0\0\0\0\0\0\0\0", pad=None, padmode=pyDes.PAD_PKCS5)
  encrypted_data = k.encrypt(file_contents)
  conn.put_object("original_files", file_name, contents = str(encrypted_data), content_type="plain/text")
  return 'File Uploaded'


@app.route('/download', methods=['GET', 'POST'])
def download_file():
  file = request.args.get('file_name', '')
  key = request.args.get('key','')
  if len(file) > 1:
    obj_tuple = conn.get_object("original_files", file)
    with open("keys.txt", "r") as info:
      information = info.read()
    information = information.split(";")
    for data in information:
      if (file in data) & ("original_files" in data):
        data = data.split(" ")
        if key == data[2] :
          temp_key = key_processing(key)
          k = pyDes.des(bytes(temp_key), pyDes.CBC, b"\0\0\0\0\0\0\0\0", pad=None, padmode=pyDes.PAD_PKCS5)
          decrypted_file_Contents = k.decrypt(obj_tuple[1])
          response = make_response(decrypted_file_Contents)
          response.headers["Content-Disposition"] = "attachment; filename=" + file
          return response
    return "Decryption key did not match"
  else:
    return 'No File Selected'


@app.route('/list', methods=['GET', 'POST'])
def list_file():
  list = ''
  for container in conn.get_account()[1]:
    for data in conn.get_container(container['name'])[1]:
      list = list + '<li>' + container['name'] + ' : ' + '{0}\t{1}\t{2}'.format(data['name'], data['bytes'],
                                                            data['last_modified']) + "</li><br>"
  return list


@app.route('/delete', methods=['GET', 'POST'])
def delete_file():
  file = request.args.get('file_name', '')
  if len(file) > 1:
    obj = conn.get_object("original_files", file)
    conn.delete_object("original_files", file)
    for data in conn.get_container("backup_files")[1]:
      if str(data['name']) == file:
        obj_tuple = conn.get_object("backup_files", file)
        conn.put_object("original_files", file, contents=obj_tuple[1], content_type="plain/text")
        conn.delete_object("backup_files", file)
    conn.put_object("backup_files", file, contents=obj[1], content_type="plain/text")
    with open("key.txt", "r") as info :
      information = info.read()
    with open("key.txt", "w") as info:
      info.write("")
    information = information.split(";")
    with open("keys.txt", "a") as keyfile:
      for dat in information:
        if (file in dat) & ("backup_files" in dat):
          data = string.replace(dat, "backup_files", "original_files")
        elif (file in dat) & ("original_files" in dat):
          data = string.replace(dat, "original_files", "backup_files")
        if len(data) > 5:
          keyfile.write(data + " ;")
    return 'File Deleted'
  else:
    return 'No File Selected'


@app.route('/')
def first_page():
  return app.send_static_file('index.html')

port = os.getenv('PORT', '7000')
if __name__ == "__main__":
  app.run(host='0.0.0.0', port=int(port))