import pyuac
import os, sys, shutil, datefinder

# filename = 'test.txt'
# src = 'C:/Users/geekh/Desktop/file-classifier/test/'
# targetDir = 'C:/Users/geekh/Desktop/file-classifier/test2/'

# shutil.copy2(src + filename, targetDir + filename)
# print(os.getcwd())


# Function that create dir
def make_dir(name):
    if not os.path.isdir(name):
        os.makedirs(name)
        print(name, "폴더가 생성되었습니다.")
    else:
        print("해당 폴더가 이미 존재합니다.")



if not pyuac.isUserAdmin():
    pyuac.runAsAdmin()

# Change current directory to PATH at the CMD, then print current dir and file list in dir
PATH = "C:/Users/geekh/Desktop/file-classifier/test/"
os.chdir(PATH)
print("현재 위치: ", os.getcwd())

files = os.listdir(PATH)
print("현재 위치 파일 리스트: ", files)

# Rename the files without file extension in PATH
withoutFileExtension = []
for file in files:
    splitedName = file.split('.')
    if len(splitedName) >= 3:
        splitedName.pop(-1)
        name = ""
        for n in range(0, len(splitedName)):
            if n != len(splitedName)-1:
                name += splitedName[n] + "."
            else:
                name += splitedName[n]
        withoutFileExtension.append(name)
    else:
        withoutFileExtension.append(splitedName[0])

print("확장자 제거한 파일 이름 리스트: ", withoutFileExtension)


# Function that find dates which pattern is like 'YYMMDD'
def findDates(file_name):
    file_nums = []
    num_element = ""
    for n in range(1, len(file_name)+1):
        if n == len(file_name):
            if file_name[n-1].isdecimal():
                num_element += file_name[n-1]
                file_nums.append(num_element)
        else:
            if file_name[n-1].isdecimal():
                if file_name[n].isdecimal():
                    num_element += file_name[n-1]
                else:
                    num_element += file_name[n-1]
                    file_nums.append(num_element)
                    num_element = ""
                    continue
    return file_nums
    
""" 작 업 중 """
def isYYMMDD(file_num):
    dates = []
    for num in file_num:
        if len(num) == 6:
            dates.append(num)
        else:
            return False

    if len(dates) == 1:
        date = dates[0]
        YY = int(date[0] + date[1])
        MM = int(date[2] + date[3])
        DD = int(date[4] + date[5])
        if 1 <= MM <= 12:
            if 1 <= DD <= 31:
                if YY > 20:
                    return ("19" + str(YY))
                else:
                    return ("20" + str(YY))
            else:
                return False
        else:
            return False

# Find dates using the 'datefinder' module
matches = datefinder.find_dates(withoutFileExtension[3])

for match in matches:
    print(match)