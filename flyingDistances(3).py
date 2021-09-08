import math

# 1a Translate the haversine function into python code. I have split it up in four parts.
def haversine(lat1, long1, lat2, long2):
    sineLats = math.sin((lat2 - lat1) / 2) ** 2
    cosLats = math.cos(lat1) * math.cos(lat2)
    sineLongs = math.sin((long2 - long1) / 2) ** 2
    a2 = sineLats + cosLats * sineLongs
    a = math.sqrt(a2)

    b = math.sqrt(1 - a2)

    d = 2 * math.atan2(a, b)

    return d


# 1b Convert degrees into decimal degrees and then the radians.
def radConvert(sign, degrees, minutes):
    degreeMinutes = minutes/60
    radians = (degrees + degreeMinutes) * math.pi/180 * sign
    return radians


# 1c create the distance function. Sign: +1 = N or E, -1 = S or W
def flyingDistance(
        latDegrees1, latMinutes1, latSign1,
        longDegrees1, longMinutes1, longSign1,
        latDegrees2, latMinutes2, latSign2,
        longDegrees2, longMinutes2, longSign2
):
    # convert from degrees to radians
    latRadians1 = radConvert(latSign1, latDegrees1, latMinutes1)
    longRadians1 = radConvert(longSign1, longDegrees1, longMinutes1)
    latRadians2 = radConvert(latSign2, latDegrees2, latMinutes2)
    longRadians2 = radConvert(longSign2, longDegrees2, longMinutes2)

    distance = haversine(latRadians1, longRadians1, latRadians2, longRadians2)  # feed haversine with radians

    km = distance * 6367  # convert radians to km

    return km


def dir_translate(string): # translates direction from N, S, W, E to +1 or -1
    if string[-1] == 'N' or string[-1] == 'E':  # N or E = +1
        string = string[:-1] + '1'
    elif string[-1] == 'S' or string[-1] == 'W':  # S or W = -1
        string = string[:-1] + '-1'

    return string


def coordinate_splitter(coordinate): #split at space, check for certain conditions.
    first_space = None  # initialize to use variables for if statement
    last_space = None

    for i in range(len(coordinate)):  # iterate through string, need i for position of space
        if coordinate[i] == ' ':  # if character is space
            if first_space is None:  # make sure that first space isn't 'taken'
                first_space = i  # save position of first space
            last_space = i  # when first space is 'taken', every other space will go into last_space, this will be updated during the for loop, so the last space will remain.
    # split the string at the space-positions
    degrees = coordinate[0:first_space]
    minutes = coordinate[first_space+1:last_space]
    direction = coordinate[last_space+1:]

    # check for minutes-input. If nothing minutes is zero.
    if minutes == '':
        minutes = '0'

    # check for symbols
    if not degrees[-1].isalnum():
        degrees = degrees[:-1]

    if not minutes[-1].isalnum():
        minutes = minutes[:-1]

    # return from function
    return degrees, minutes, direction


# coordinates of departure destination
lat1 = input('Latitude of departure: ').upper()
long1 = input('Longitude of departure: ').upper()

# coordinates of arrival destination
lat2 = input('Latitude of destination: ').upper()
long2 = input('Longitude of destination: ').upper()

# translate direction into sign to use in haversine-formula
lat1 = dir_translate(lat1)
long1 = dir_translate(long1)
lat2 = dir_translate(lat2)
long2 = dir_translate(long2)

# split coordinates into variables
latDegrees1, latMinutes1, latDir1 = coordinate_splitter(lat1)
longDegrees1, longMinutes1, longDir1 = coordinate_splitter(long1)
latDegrees2, latMinutes2, latDir2 = coordinate_splitter(lat2)
longDegrees2, longMinutes2, longDir2 = coordinate_splitter(long2)

# convert to integers
int_convert = []
latDegrees1, latMinutes1, latDir1 = int(latDegrees1), int(latMinutes1), int(latDir1)
longDegrees1, longMinutes1, longDir1 = int(longDegrees1), int(longMinutes1), int(longDir1)
latDegrees2, latMinutes2, latDir2 = int(latDegrees2), int(latMinutes2), int(latDir2)
longDegrees2, longMinutes2, longDir2 = int(longDegrees2), int(longMinutes2), int(longDir2)

# call function with parameters in int
distance = flyingDistance(
    latDegrees1, latMinutes1, latDir1,
    longDegrees1, longMinutes1, longDir1,
    latDegrees2, latMinutes2, latDir2,
    longDegrees2, longMinutes2, longDir2
)

print(round(distance, 4), 'km')