import httplib2

'''
1. Download file and read file.
2. Calculate average price per month for google stock by using formula:  ((v1 * c1) + (v2 * c2) + (v3 * c3) + (v4 * c4) ... (vn * cn) + ) / (v1+v2+v3+v4...+vn)
    where vi is the volume for day i and ci is the adjusted close price for day i.
3. Sort them and print top and bottom six months.
'''

#Globals
DATA_URL = "https://dl.dropboxusercontent.com/u/15507637/googlePrices.csv"
data_set = []
average_list = []
year_start = 2004
year_end = 2012


def average(data, month, year):
    ''' Function to calculate average stock price '''
    vol = 0
    total = 0
    for volume in data_set:
        if volume[0][1:5] == year:  # Slice list of list
            if volume[0][6:8] == month:
                vol += volume[1]
                total += (volume[1] * volume[2])
    average = total/vol
    return average, month +'-'+ year  # Tuple of average, month and year.


def main():
    ''' 1. Read data pull date, volume and adj columns.
        2. Call average function pass apropriate arguments.
        3. Get averages append them to average_list.
        4. Sort and reverse average_list.
        5. Using slice print top and bottom 6.
'''
    try:
        h = httplib2.Http(".cache")
        headers, fh = h.request(DATA_URL)
        fh = fh.decode().split('\n')  # Convert bytes to String
        for line in fh:
            try:
                line_list = line.split(',')
                date = line_list[0]
                volume = float(line_list[5])  #  Convert volume to float
                adj = float(line_list[6])     #  Convert volume to adj
                data_set.append([date, volume, adj])  # Append to data set.
            except ValueError:  # First line is String in data to catch ValueError.
                continue
            except IndexError:  
                continue

        months = []
        global year_start  # Global variable value is changing inside main function.
        for i in range(12):  #  Generating months 0 to 12 like (00, 01, 02 ... 12) in string to pass as arguments in the average() function.
            if i < 9:
                months.append(str(0) + str(i+1))    
            else:
                months.append(str(i+1))

        while(year_start <= year_end):
            for m in months:
                try:
                    average_list.append(average(data_set, m, str(year_start)))  #  Apending average stock prices.
                except ZeroDivisionError:
                    continue
            year_start += 1
            
    #  Pretty print my own version down below.
        print('Top six: ')
        print('Average','\t\t', 'Mon/Year')
        for data in reversed(sorted(average_list[-6:])):
            print("{:.2f} \t\t\t {}".format(data[0], data[1]))
            
        print()

        print('Bottom six: ')
        print('Average','\t\t', 'Mon/Year')
        for data in reversed(sorted(average_list[:6])):
             print("{:.2f} \t\t\t {}".format(data[0], data[1]))
    except IOError as e:
        print(e)

if __name__ == '__main__':
    main()
