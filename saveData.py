import csv 
import datetime
import os
import notify

def addNewRow(isApproved, videoPath,hodorTime):
    row = ['?','?','?','?','?','?']
    f = open('contSize.txt' , 'r')
    contourVal = int(f.readline())
    f.close()
    Dtime = datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p")
    day = datetime.datetime.now().strftime("%A")
    time = datetime.datetime.now().strftime("%I:%M:%S%p")
    date = datetime.datetime.now().strftime("%d %B %Y")
    with open('AlertRate.csv', "r", encoding="utf-8", errors="ignore") as f_object:
        final_line = f_object.readlines()[-1]
        f_object.close()

    try:
        AlertNo = int(final_line.split(',')[0])
        AlertNo = AlertNo + 1
    except:
        AlertNo = 0
    print(AlertNo)
    filename = str(AlertNo) + '_' + date.replace(" ", "") + '_' + str(isApproved) + '.mp4'
    if isApproved:
        os.rename(videoPath,r'./assets/approvedVid/' + filename)
        local_file = './assets/approvedVid/' + filename
        notify.upload_to_aws(local_file, filename)
    else:
        os.rename(videoPath,r'./assets/rejectedVid/' + filename)
    row = [AlertNo,isApproved,contourVal,time,day,date,filename,hodorTime]
    with open('AlertRate.csv', 'a+', newline='') as f_object:
        writer_object = csv.writer(f_object)
        writer_object.writerow(row)
        f_object.close()
        print(row)