import pyuac, datefinder # 외장
import os, sys, shutil, datetime # 내장

# filename = 'test.txt'
# src = 'C:/Users/geekh/Desktop/file-classifier/test/'
# targetDir = 'C:/Users/geekh/Desktop/file-classifier/test2/'

# shutil.copy2(src + filename, targetDir + filename)
# print(os.getcwd())


# Function that create dir
def make_dir(name):
    try:
        if not(os.path.isdir(name)):
            os.makedirs(os.path.join(name))
    except OSError as e:
        if e.errno != errno.EEXIST:
            print("Failed to create directory!!!!!")
            raise


# find numbers in files' name
def findNums(file_name):
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
    if len(file_nums) == 0:
        return False
    return file_nums
    
# check the returned number from findNums(file_name) that is 'YYMMDD' format
def isYYMMDD(file_nums):
    dates = []
    for num in file_nums:
        if len(num) == 6:
            dates.append(num)
        else:
            return False

    date = dates[0] #if there are more than two elements(6 length) in 'date' list, check the first element
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


# Find year in dates using the 'datefinder' module
def dateFinderModule(file_name):
    matches = datefinder.find_dates(file_name)
    dates = []
    for match in matches:
        dates.append(match)

    # one date element and return the year
    if len(dates) == 1:
        date = dates[0]
        strDate = str(date)
        year = strDate[0:4]
        return year

    # more than two date elements and return the recent year
    elif len(dates) > 1:
        yearList = []
        for date in dates:
            year = str(date)[0:4]
            yearList.append(int(year))
        yearList.sort()
        selectedYear = str(yearList[-1])
        return selectedYear

    # there is no date
    else:
        return False

# Find year from create date in file system info
def fileInfo(file_name):
    ctime = os.path.getctime(file_name)
    time = datetime.datetime.fromtimestamp(ctime)
    strTime = str(time)
    year = strTime[0:4]
    return year

# # Rename the files without file extension
# withoutFileExtension = []
# for file in files:
#     splitedName = file.split('.')
#     if len(splitedName) >= 3:
#         splitedName.pop(-1)
#         name = ""
#         for n in range(0, len(splitedName)):
#             if n != len(splitedName)-1:
#                 name += splitedName[n] + "."
#             else:
#                 name += splitedName[n]
#         withoutFileExtension.append(name)
#     else:
#         withoutFileExtension.append(splitedName[0])
# print("File names without File Extension: ", withoutFileExtension)


"""
    the flow of Finding Dates in file names
    First, check file names with YYMMDD check function (findNums() -> isYYMMDD())
    if first result is false, Second, check file names with datefinder module fuction (dateFinderMoudle)
    if second result is false, Third, check the created time in file system info (fileInfo())
"""

# this python file gets Administrator
if not pyuac.isUserAdmin():
    pyuac.runAsAdmin()

# Change current directory to PATH at the CMD, then print current dir and file list in dir
PATH = "C:/Users/geekh/Desktop/file-classifier/test/"
os.chdir(PATH)
print("Current Dir: ")
print(os.getcwd())

files = os.listdir(PATH)
print("Files in Current Dir: ")
print(files)

# dictYear = {'year' : ['file_name01', 'file_name02'...]} (Dictionary type)
dictYear = {}

for file_name in files:
    # First 
    file_nums = findNums(file_name)
    if file_nums is False:
        # Third
        year = fileInfo(file_name)
        if year not in dictYear:
            dictYear[year] = []
            dictYear[year].append(file_name)
        else:
            dictYear[year].append(file_name)
    else:
        year = isYYMMDD(file_nums)
        if year is not False:
            if year not in dictYear:
                dictYear[year] = []
                dictYear[year].append(file_name)
            else:
                dictYear[year].append(file_name)
        else:
            # Second
            year = dateFinderModule(file_name)
            if year is not False:
                if year not in dictYear:
                    dictYear[year] = []
                    dictYear[year].append(file_name)
                else:
                    dictYear[year].append(file_name)
            else:
                print("ERROR")

years = list(dictYear.keys())
print("detected years: ")
print(years)

# create TARGET DIRECTORY (name: PATH directory name + by file classifier)
FINAL_DIR_PATH = PATH[-5:-1]
TARGET_DIR = FINAL_DIR_PATH + "_by_file_classifier"
make_dir(TARGET_DIR)

# change current directory to TARGET DIRECTORY at the CMD
CHPATH = PATH + TARGET_DIR + "/"
os.chdir(CHPATH)
print(os.getcwd())

# make each year's directory
for year in years:
    make_dir(year)
    for file in dictYear[year]:
        try:
            shutil.copy2(PATH+file, CHPATH+year+"/")
        except PermissionError:
            pass