import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }


def get_filters():
    """
    Asks user to specify a city and a filter to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) filter - type of filter
    """
    print("Welcome! Let's explore some US BikeShare data!")

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = str(input("Would you like to see data for Chicago, New York or Washington? ")).lower()

    #Repeat until correct information is input
    while True:
        if (city == "chicago" or city == "new york" or city == "washington"):
            print(CITY_DATA[city])
            break
        else:
            city = str(input("Please enter a valid name: Chicago, New York or Washington or press CRL + C to quit ")).lower()

    # get user input for filter
    selected_filter = str(input("Would you like to filter the data by month, day, both or not at all? Type \"none\" for no time filter: " )).lower()
    while True:
        if selected_filter == "month" or selected_filter == "day" or selected_filter == "both" or selected_filter == "none":
            break
        else:
            selected_filter = str(input("Please select one of the following to filter your data: month, day, both, \"none\" for no time filter or press CRL + C to quit : " )).lower()
    print('-'*40)
    return city, selected_filter



def get_data(city, selected_filter):
    """ Requests city and filters and returns filtered dataset """

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['hour'] = df['Start Time'].dt.hour
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    if selected_filter == "month":
        month = which_month()
        day = 'all'
        df = df[df['month'] == month]
        return df, day, month
    elif selected_filter == "day":
        month = 'all'
        day = which_day()
        df = df[df['day_of_week'] == day]
        return df, day, month
    elif selected_filter == "both":
        month = which_month()
        day =which_day()
        df = df[df['month'] == month]
        df = df[df['day_of_week'] == day]
        return df, day, month
    elif selected_filter == "none":
        month = 'all'
        day = 'all'
        return df, day, month



def which_month():
    """ Requests input Month and returns month's index """
    month = 0
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    selected_month = str(input("Which month? January, February, March, April, May, June: " )).lower()
    while True:
        if selected_month in months:
            month = months.index(selected_month) + 1
            return month
            break
        else:
            selected_month = str(input("Select one of the following: January, February, March, April, May, June: or press CRL + C to quit " )).lower()


def which_day():
    """ Requests input Day and returns name of Day """
    day = 0
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    selected_day = str(input("Which day? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday: " )).lower()
    while True:
        if selected_day in days:
            day = selected_day.title()
            return day
            break
        else:
            selected_day = str(input("Select one of the following: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday: or press CRL + C to quit " )).lower()


def time_stats(df, day, month, city, selected_filter):
    """Displays statistics on the most frequent times of travel."""

    print('-'*40 + '\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    months = ['January', 'February', 'March', 'April', 'May', 'June']

    #Returns the most common month in dataset
    common_month = df['month'].mode()[0]
    #Returns the most common day in dataset
    common_day = df['day_of_week'].mode()[0]
    #Returns the most common hour in dataset
    common_hour = df['hour'].mode()[0]

    #Returns the frequency of each month in dataset
    month_count = pd.DataFrame(df['month'].value_counts())
    #Returns the frequency of each day in selected month
    day_count = pd.DataFrame(df['day_of_week'].value_counts())
    #Returns the frequency of each hour in dataset
    hour_count = pd.DataFrame(df['hour'].value_counts())

    #Returns the frequency of most common month in dataset
    max_month_count = month_count['month'].iloc[0]
    #Returns the frequency of most common day in dataset
    max_day_count = day_count['day_of_week'].iloc[0]
    #Returns the frequency of most common hour in dataset
    max_hour_count = hour_count['hour'].iloc[0]

    #Print appropriate statistics based on applied filter
    if selected_filter == 'month':
        print("The most common day for {} in {} was {}. (Count: {}).".format(months[month - 1], city.title(), common_day, max_day_count))
        print("The most common hour for {} in {} was {}:00h. (Count: {})".format(months[month - 1], city.title(), common_hour, max_hour_count))
        print("(Filter: {})".format(selected_filter.title()))
    elif selected_filter == 'day':
        print("The most common month for {} in {} was {}. (Count: {})".format(day, city.title(), months[common_month - 1], max_month_count))
        print("The most common hour for {} in {} was {}:00h. (Count: {})".format(day, city.title(), common_hour,max_hour_count))
        print("(Filter: {})".format(selected_filter.title()))
    elif selected_filter == 'both':
        print("The most common hour on {} for {} in {} was {}:00h. (Count: {})".format(day, months[month - 1], city.title(), common_hour, max_hour_count))
        print("(Filter: {})".format(selected_filter.title()))
    else:
        print("The most common month in {} was {}. (Count: {})".format(city.title(), months[common_month - 1], max_month_count))
        print("The most common day in {} was {}. (Count: {})".format(city.title(), common_day, max_day_count))
        print("The most common hour in {} was {}:00h. (Count: {})".format(city.title(), common_hour, max_hour_count))
        print("(Filter: {})".format(selected_filter.title()))
    #Print calculation time
    if (time.time() - start_time) < 1:
        print("\nThis calculation took less than 1 second.")
    else:
        print("\nThis calculation took %s seconds." % (time.time() - start_time))
    print('-'*40)




def station_stats(df, day, month, city, selected_filter):
    """Displays statistics on the most popular stations and trip. """

    #print(df)
    print('-'*40 + '\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    months = ['January', 'February', 'March', 'April', 'May', 'June']

    #Creates a DataFrame grouped by Start Station and creates a column 'Count' with value counts
    ds = pd.DataFrame({'Count': df.groupby( ['Start Station'] ).size().sort_values(ascending=False)}).reset_index()
    common_start_station = ds['Start Station'].iloc[0]
    #Returns the frequency of most common Start Station in dataset
    max_start_station_count = ds['Count'].iloc[0]


    #Creates a DataFrame grouped by End Station and creates a column 'Count' with value counts
    de = pd.DataFrame({'Count': df.groupby( ['End Station'] ).size().sort_values(ascending=False)}).reset_index()
    common_end_station = de['End Station'].iloc[0]
    #Returns the frequency of most common End Station in dataset
    max_end_station_count = de['Count'].iloc[0]


    #Creates a DataFrame grouped by Start and End Station and creates a column 'Count' with value counts
    dm = pd.DataFrame({'Count': df.groupby( ['Start Station', 'End Station'] ).size().sort_values(ascending=False)}).reset_index()
    comb_start_station = dm['Start Station'].iloc[0]
    comb_end_station = dm['End Station'].iloc[0]
    comb_count = dm['Count'].iloc[0]


    if selected_filter == 'month':
        print("The most common Start Station in {} on {} was {}. (Count: {})".format(city.title(), months[month - 1], common_start_station, max_start_station_count))
        print("The most common End Station in {} on {} was {}. (Count: {})".format(city.title(), months[month - 1], common_end_station, max_end_station_count))
        print("The most common Start & End Station combination in {} on {} was {} - {}. (Count: {})".format(city.title(), months[month - 1], comb_start_station, comb_end_station, comb_count))
        print("(Filter: {})".format(selected_filter.title()))
    elif selected_filter == 'day':
        print("The most common Start Station for {} in {} was {}. (Count: {})".format(day, city.title(), common_start_station, max_start_station_count))
        print("The most common End Station for {} in {} was {}. (Count: {})".format(day, city.title(), common_end_station, max_end_station_count))
        print("The most common Start & End Station combination for {} in {} was {} - {}. (Count: {})".format(day, city.title(), comb_start_station, comb_end_station, comb_count))
        print("(Filter: {})".format(selected_filter.title()))
    elif selected_filter == 'both':
        print("The most common Start Station on {} for {} in {} was {}. (Count: {})".format(day, months[month - 1], city.title(), common_start_station, max_start_station_count))
        print("The most common End Station on {} for {} in {} was {}. (Count: {})".format(day, months[month - 1], city.title(), common_end_station, max_end_station_count))
        print("The most common Start & End Station combination on {} for {} in {} was {} - {}. (Count: {})".format(day, months[month - 1], city.title(), comb_start_station, comb_end_station, comb_count))
        print("(Filter: {})".format(selected_filter.title()))
    else:
        print("The most common Start Station in {} was {}. (Count: {})".format(city.title(), common_start_station, max_start_station_count))
        print("The most common End Station in {} was {}. (Count: {})".format(city.title(), common_end_station, max_end_station_count))
        print("The most common Start & End Station combination in {} was {} - {}. (Count: {})".format(city.title(), comb_start_station, comb_end_station, comb_count))
        print("(Filter: {})".format(selected_filter.title()))

    #Print calculation time
    if (time.time() - start_time) < 1:
        print("\nThis calculation took less than 1 second.")
    else:
        print("\nThis calculation took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('-'*40 + '\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time_sec = df['Trip Duration'].sum()
    total_travel_time_min = int(total_travel_time_sec/60)
    print("The total travel time was {}min".format(total_travel_time_min))
    # display mean travel time
    mean_travel_time_sec = df['Trip Duration'].mean()
    mean_travel_time_min = int(mean_travel_time_sec/60)
    print("The average travel time was {}min".format(mean_travel_time_min))

    #Print calculation time
    if (time.time() - start_time) < 1:
        print("\nThis calculation took less than 1 second.")
    else:
        print("\nThis calculation took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('-'*40 + '\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    df = df.dropna()
    du = pd.DataFrame({'Count': df.groupby( ['User Type'] ).size().sort_values(ascending=False)}).reset_index()
    print(du.to_string(index=False))

    # Display counts of gender

    if city == 'chicago'or city == 'new york':
        dg = pd.DataFrame({'Count': df.groupby( ['Gender'] ).size().sort_values(ascending=False)}).reset_index()
        print('\n' + dg.to_string(index=False))

    # Display earliest, most recent, and most common year of birth
    if city == 'chicago'or city == 'new york':
        db = pd.DataFrame({'Count': df.groupby( ['Birth Year'] ).size().sort_values(ascending=False)}).reset_index()
        print('\n' + 'Earliest Birth Year: ' + str(int(db['Birth Year'].min())))
        print('Most Recent Birth Year: ' + str(int(db['Birth Year'].max())))
        print('Most Common Birth Year: ' + str(int(db['Birth Year'].iloc[0])))


    #Print calculation time
    if (time.time() - start_time) < 1:
        print("\nThis calculation took less than 1 second.")
    else:
        print("\nThis calculation took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_input(df):
    """ Asks user if he wants to see raw input and how many rows """
    raw_answer = str(input("Would you like to see the row results? (Yes/No): ")).lower()
    result_no = 0
    while True:
        if raw_answer == 'yes':
            start = 0
            try:
                row_number = int(input("How many rows? Type integer between 1 and 10: "))
                if row_number > 0 and row_number <= 10:
                    result_no = row_number
                    while raw_answer == 'yes':
                        print(df.iloc[ start : row_number,:])
                        start = row_number
                        row_number += result_no
                        raw_answer = str(input("Would you like to see the next {} results? (Yes/No): ".format(result_no))).lower()
                    else:
                        raw_answer = str(input("Please type \"Yes\" to see the next {} results or \"No\" to quit. ".format(result_no))).lower()
            except ValueError:
                continue
        elif raw_answer == 'no':
            break
        else:
            raw_answer = str(input("Please type \"Yes\" to see raw results or \"No\" to quit. ")).lower()



def main():
    while True:
        city, selected_filter = get_filters()
        df, day, month = get_data(city, selected_filter)

        time_stats(df, day, month, city, selected_filter)
        station_stats(df, day, month, city, selected_filter)
        trip_duration_stats(df)
        user_stats(df, city)
        raw_input(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
