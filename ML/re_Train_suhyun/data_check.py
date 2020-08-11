
import os

path = "Sign-Language-Digits-Dataset/Dataset/"
file_list = os.listdir(path)
file_list.sort()
for i in file_list:
    temp_file_list=os.listdir(path+i)
    print(i," : ",len(temp_file_list))