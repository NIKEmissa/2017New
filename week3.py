import datetime
from pygeodesy import ellipsoidalVincenty as ev

with open("/Users/isobel_shen/PycharmProjects/Week3/hurdat2-1851-2016-041117.txt", "r") as f:
    Hurricane = f.readlines()


def record_highest_msw():
    """
    This function is used to:
     1.print HMSW on console
     2.record HMSW into Hurdict
     3.and when it occurred
    :return:
    """
    Highest_MSW = 0
    for target in Hurricane[start_line:end_line]:  # handle with content(each Hurricane)
        if int(target[38:41]) > Highest_MSW:  # get Highest Maximum sustained wind
            Highest_MSW = int(target[38:41])

    print('Highest Maximum Sustained Wind: {HMSW} Knots'.format(HMSW=str(Highest_MSW)))
    Hurdict[Storm_system_name]['Highest Maximum Sustained Wind'] = {'Wind Speed': str(Highest_MSW) + 'Knots'}

    Hurdict[Storm_system_name]['Highest Maximum Sustained Wind']['D&T'] = []
    for targets in Hurricane[start_line:end_line]:  # record when did it happen
        if int(targets[38:41]) == Highest_MSW:
            print('Date: {DATE}; Time: {TIME}'.format(DATE=str(targets[:8]), TIME=str(targets[10:14])))
            Hurdict[Storm_system_name]["Highest Maximum Sustained Wind"]['D&T'] += \
                [str(targets[:8]) + str(targets[10:14])]


def number_storm_hurricane():
    """
    How many storms and Hurricanes happened in a year
    :return:
    """
    zero = len(storm_years()) * [0]
    stormandhurr = dict(zip(storm_years(), zero))
    for years in storm_years():
        stormandhurr[years] = {'Storm': 0, 'Hurricane': 0}
        for keyvalue in Hurdict.keys():
            if keyvalue[4:8] == years:
                stormandhurr[years]['Storm'] += 1
                if Hurdict[keyvalue]['Level']['Hurricane'] == 'Y':
                    stormandhurr[years]['Hurricane'] += 1
    Hurdict['Number of storm and hurricane'] = stormandhurr


def if_Sto_and_Hur():
    """
    detect a system if it is a Storm or a Hurricane or both.
    :return:
    """
    Hurdict[Storm_system_name]['Level'] = {'Storm': 'Y'}
    Hurdict[Storm_system_name]['Level']['Hurricane'] = 'N'
    for target in Hurricane[start_line:end_line]:  # handle with content(each Hurricane)
        if target[19:21] == 'HU':
            Hurdict[Storm_system_name]['Level']['Hurricane'] = 'Y'


def storm_years():
    """This function is for counting which year appears storm

    :return years
    """
    years = []
    for aline in Hurricane[:]:

        if len(aline.split(sep=',')) == 4:
            if str(aline[4:8]) not in years:
                years.append(str(aline[4:8]))
    return years


def calculate_time(startline, endline):
    """
    calculate time span between two samples
    :param startline:first sample
    :param endline:second sample
    :return:time span(unit: seconds)
    """
    HS = Hurricane[startline]
    starttime = datetime.datetime(int(HS[0:4]), int(HS[4:6]), int(HS[6:8]), int(HS[10:12]), int(HS[12:14]))
    HE = Hurricane[endline]
    endtime = datetime.datetime(int(HE[0:4]), int(HE[4:6]), int(HE[6:8]), int(HE[10:12]), int(HE[12:14]))

    seconds = (endtime - starttime).days * 24 * 3600 + (endtime - starttime).seconds
    return seconds


def calculate_distance(startline):
    """
    calculate distance between start sample and next
    :param startline: start sample
    :return: distance(meter)
    """
    HS = Hurricane[startline]
    startpoint = ev.LatLon(HS[23:28], HS[30:36])
    HE = Hurricane[startline + 1]
    endpoint = ev.LatLon(HE[23:28], HE[30:36])

    if startpoint == endpoint:
        delta = 0
    else:
        delta = startpoint.distanceTo3(endpoint)[0]
    return delta


def storm_maximum_mean_speed(begain_line, finish_line):
    """
    calculate the maximum speed and the mean speed for a storm system
    :param begain_line:system begin line
    :param finish_line:system end line + 1
    :return:
    """
    maximum_speed = 0
    total_distance = 0
    if finish_line - begain_line > 1:
        for i in range(begain_line, finish_line - 1):
            # print(Hurricane[i])
            storm_speed = calculate_distance(i) / calculate_time(i, i + 1)
            total_distance += calculate_distance(i)  # return total_distance for a storm
            if storm_speed > maximum_speed:
                maximum_speed = storm_speed

        mean_speed = total_distance / calculate_time(begain_line, finish_line - 1)
        Hurdict[Storm_system_name]['Maximum Speed(Knots)'] = maximum_speed * 1.94384
        Hurdict[Storm_system_name]['Mean Speed(Knots)'] = mean_speed * 1.94384
        Hurdict[Storm_system_name]['Total distance tracked(Nautical mile)'] = total_distance * 0.000539957

    elif finish_line - begain_line == 1:
        maximum_speed = None
        mean_speed = None
        Hurdict[Storm_system_name]['Maximum Speed(Knots)'] = maximum_speed
        Hurdict[Storm_system_name]['Mean Speed(Knots)'] = mean_speed


def calculate_bearing(startline, endline):
    HS = Hurricane[startline]
    startpoint = ev.LatLon(HS[23:28], HS[30:36])
    HE = Hurricane[endline]
    endpoint = ev.LatLon(HE[23:28], HE[30:36])

    if startpoint == endpoint:
        delta = None
        # print('我们相等')
        return delta
    else:
        delta = startpoint.distanceTo3(endpoint)
        return delta[1:]


def storm_bearing_summary(begain_line, finish_line):
    Hurdict[Storm_system_name]['Bearing'] = {}
    Hurdict[Storm_system_name]['Bearing']['Samples'] = {}
    Hurdict[Storm_system_name]['Bearing']['Direction Change'] = {}

    if finish_line - begain_line > 1:
        if calculate_bearing(begain_line, finish_line-1):
            average_bearing_system = (calculate_bearing(begain_line, finish_line-1)[0]
                                      + calculate_bearing(begain_line, finish_line - 1)[1])/2
            Hurdict[Storm_system_name]['Bearing']['System'] = average_bearing_system
        else:
            Hurdict[Storm_system_name]['Bearing']['System'] = None

        for i in range(begain_line, finish_line - 1):
            if calculate_bearing(i, i+1):
                average_bearing_sample = (calculate_bearing(i, i+1)[0] + calculate_bearing(i, i+1)[1]) / 2
                # print(average_bearing_sample)
                Hurdict[Storm_system_name]['Bearing']['Samples'][
                    Hurricane[i][0:8] + Hurricane[i][10:14]] = average_bearing_sample

                time_interval = calculate_time(i, i+1)
                direction_change = abs(calculate_bearing(i, i+1)[0] - calculate_bearing(i, i+1)[1]) / time_interval
                Hurdict[Storm_system_name]['Bearing']['Direction Change'][
                    Hurricane[i][0:8] + Hurricane[i][10:14]] = direction_change

                # print(direction_change)
            else:
                # print('None')
                Hurdict[Storm_system_name]['Bearing']['Samples'][
                    Hurricane[i][0:8] + Hurricane[i][10:14]] = None
                Hurdict[Storm_system_name]['Bearing']['Direction Change'][
                    Hurricane[i][0:8] + Hurricane[i][10:14]] = None

    elif finish_line - begain_line == 1:
        # print('None')
        Hurdict[Storm_system_name]['Bearing']['Samples'][
            Hurricane[begain_line][0:8] + Hurricane[begain_line][10:14]] = None
        Hurdict[Storm_system_name]['Bearing']['System'] = None
        Hurdict[Storm_system_name]['Bearing']['Direction Change'][
            Hurricane[begain_line][0:8] + Hurricane[begain_line][10:14]] = None


def count_landfalls(begin_line, finish_line):
    Landfalls = 0
    Hurdict[Storm_system_name]['Landfall'] = {}
    Hurdict[Storm_system_name]['Landfall']['D&T'] = []
    for target in Hurricane[begin_line:finish_line]:
        if target[16] == 'L':
            Landfalls += 1
            Hurdict[Storm_system_name]['Landfall']['D&T'] += [target[0:8] + target[10:14]]

    Hurdict[Storm_system_name]['Landfall']['Times'] = Landfalls
    print('Landfalls: {}'.format(Landfalls))


def biggest_change() -> list:
    # print(Hurdict[Storm_system_name]['Bearing']['Direction Change'])
    biggest_value_change = 0.0
    datevalue = None
    # if Hurdict[Storm_system_name]['Bearing']['Direction Change'] != None:
    #     print(list(Hurdict[Storm_system_name]['Bearing']['Direction Change'].values()))
    for item in Hurdict[Storm_system_name]['Bearing']['Direction Change']:
        # print(item)
        if Hurdict[Storm_system_name]['Bearing']['Direction Change'][item]:
            if Hurdict[Storm_system_name]['Bearing']['Direction Change'][item] > biggest_value_change:
                biggest_value_change = Hurdict[Storm_system_name]['Bearing']['Direction Change'][item]
                datevalue = item
    # return print('Biggest Change:', biggest_value_change, 'Date:', datevalue, '\n')
    #         # print(item)
    #         # print(type(biggest_value_change))
    #         if item > biggest_value_change:
    #             biggest_value_change = item
    # return biggest_value_change
    if Hurdict[Storm_system_name]['Landfall']['Times'] != 0:
        if datevalue == Hurdict[Storm_system_name]['Landfall']['D&T'][0]:
            find_out_cp['count'] += 1
            find_out_cp['amount'] += 1
        else:
            find_out_cp['amount'] += 1
    return [biggest_value_change, datevalue]


# def find_out_change_percentage():


Hurdict = {}
DateRange = {}
find_out_cp = {'count': 0, 'amount': 0}
start_line = 1
for line in Hurricane[:]:
    # print(len(line))
    if len(line.split(sep=",")) == 4:  # select header; handle with header
        Storm_system_name = str(line)[:8] + str(line)[18:28]  # pick up names
        print(Storm_system_name)

        number_lines = int(line.split(sep=",")[2])  # count how many lines for each hurricane
        end_line = start_line + number_lines

        Date_range = Hurricane[start_line][:8] + " to " + Hurricane[end_line - 1][:8]  # count date range
        print(Date_range)
        DateRange['Start'] = Hurricane[start_line][:8]
        DateRange['End'] = Hurricane[end_line - 1][:8]
        Hurdict[Storm_system_name] = {'DateRange': DateRange}

        record_highest_msw()
        if_Sto_and_Hur()
        count_landfalls(start_line, end_line)
        storm_maximum_mean_speed(start_line, end_line)
        storm_bearing_summary(start_line, end_line)
        print('Biggest Change:', biggest_change()[0], 'Date:', biggest_change()[1], '\n')
        # print('Biggest Change:', biggest_change(), '\n')

        start_line = end_line + 1

print(len(storm_years()))
print(Hurdict['AL022009       ANA'])
# print(Hurdict['AL051851   UNNAMED'])
print(find_out_cp)
number_storm_hurricane()
# print(Hurdict['Number of storm and hurricane'])

for line in Hurricane[:]:
    # print(len(line))
    if len(line.split(sep=",")) == 4:  # select header; handle with header
        Storm_system_name = str(line)[:8] + str(line)[18:28]  # pick up names
        print(Storm_system_name)

