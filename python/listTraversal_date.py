import datetime


def createDirPath(starttime, endtime, rootpath):
    start = datetime.datetime.strptime(starttime, "%Y%m%d%H")
    end = datetime.datetime.strptime(endtime, "%Y%m%d%H")
    dif = int((end - start).total_seconds() / 3600)  ## time difference in hours

    date_list = [((start + datetime.timedelta(hours=x)).strftime("%Y%m%d%H")) for x in range(dif + 1)]
    finalpath = []
    for i in date_list:
        datetime_object = datetime.datetime.strptime(i, "%Y%m%d%H")
        pathlist = rootpath + '/year=' + str(datetime_object.year) + '/month=' + str(datetime_object.month).rjust(2,
                                                                                                                  '0') + '/day=' + str(
            datetime_object.day).rjust(2, '0') + '/hour=' + str(datetime_object.hour).rjust(2, '0')
        finalpath.append(pathlist)
    return finalpath


if __name__ == '__main__':
    Starttime = '2018060103'
    endtime = '2018060105'
    rootpath = 'Capacity'
    Pathlist = createDirPath(Starttime, endtime, rootpath)
    print(Pathlist)

'''
input:
starttime = '2018060103'
endtime = '2018060105'
rootpath = 'Capacity'

Output:
['Capacity/year=2018/month=06/day=01/hour=03', 'Capacity/year=2018/month=06/day=01/hour=04', 'Capacity/year=2018/month=06/day=01/hour=05'
'''
