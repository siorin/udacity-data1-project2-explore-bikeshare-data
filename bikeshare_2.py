import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    cities = ['chicago', 'new york city', 'washington']
    while True:
        city = input("Enter a city - chicago, new york city, or washington : ").lower()
        if city in cities:
            break
        print('Invalid Input. Enter one of : chicago, new york city, washington')

    # get user input for month (all, january, february, ... , june)
    months = ['all', 'january', 'february', 'march', 'april', 'may', 'june', 
              'july', 'august', 'september', 'october', 'november', 'december']
    while True: 
        month = input("Enter a month - all, january, february, march, april, ... : ").lower()
        if month in months:
            break
        print('Invalid Input. Enter one of: all, january, february, march, april, may, june, july, august, september, october, november, december')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    while True:
        day = input("Enter a day of week - all, monday, tuesday, wednesday, thursday, friday, saturday, sunday : ").lower()
        if day in days:
            break
        print('Invalid Input. Enter one of: all, monday, tuesday, wednesday, thursday, friday, saturday, sunday')

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # df['day_of_week'] = df['Start Time'].dt.weekday  
    # days = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 
    #         5: 'Saturday', 6: 'Sunday'}
    # df['day_of_week'] = df['day_of_week'].apply(lambda x: days[x])

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june', 
                  'july', 'august', 'september', 'october', 'november', 'december']
        month = months.index(month) + 1
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month]
        # df = df.loc[df['month']==month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
        # df = df.loc[df['day_of_week']==day.title()]
    
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    months = ['january', 'february', 'march', 'april', 'may', 'june', 
              'july', 'august', 'september', 'october', 'november', 'december']
    mode_month = df['month'].mode()[0]
    print('Most common month: {}'.format(months[mode_month - 1]))

    # display the most common day of week
    mode_day = df['day_of_week'].mode()[0]
    print('Most common day of week: {}'.format(mode_day))

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    mode_hour = df['hour'].mode()[0]
    print('Most common start hour: {}'.format(mode_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    mode_start_st = df['Start Station'].mode()[0]
    print('Most common start station: {}'.format(mode_start_st))

    # display most commonly used end station
    mode_end_st = df['End Station'].mode()[0]
    print('Most common end station: {}'.format(mode_end_st))

    # display most frequent combination of start station and end station trip
    df['Start_End'] = df['Start Station'] + ' -> ' + df['End Station']
    mode_start_end = df['Start_End'].mode()[0]
    print('Most common combination of start and end stations: {}'.format(mode_start_end))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_time = df['Trip Duration'].sum()
    print('Total travel time: {} seconds'.format(total_time))

    # display mean travel time
    mean_time = df['Trip Duration'].mean()
    print('Mean travel time: {} seconds'.format(mean_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('Counts of user types: ')
    print(df['User Type'].value_counts())

    # Display counts of gender
    # only available for NYC and Chicago *****
    try:
        count_gender = df['Gender'].value_counts()
    except: 
        print('Selected city has no gender data')
    else: 
        print('Counts of gender: ')
        print(count_gender)

    # Display earliest, most recent, and most common year of birth
    # only available for NYC and Chicago *****
    try: 
        earliest_birth = int(df['Birth Year'].min())
        recent_birth = int(df['Birth Year'].max())
        common_birth = int(df['Birth Year'].mode()[0])
    except: 
        print('Selected city has no birth year data')
    else: 
        print('Earliest year of birth: {}'.format(earliest_birth))
        print('Most recent year of birth: {}'.format(recent_birth))
        print('Most common year of birth: {}'.format(common_birth))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

# edit 1 : added display raw data function
def display_data(df):
    """
    responses = ['yes', 'no']
    while True:
        display = input("Do you want to view the raw data? Enter yes or no : ").lower()
        if display in responses:
            break
        print('Invalid Input. Enter one of : yes, no')    
    # https://stackoverflow.com/questions/19124601/is-there-a-way-to-pretty-print-the-entire-pandas-series-dataframe
    if display == 'yes':
        with pd.option_context('display.max_rows', None, 'display.max_columns', None):
            print(df.iloc[])
    """
    # edit 2: printing additional raw data based on user input
    while True:
        display = input("Do you want to view the raw data? Enter yes or no : ").lower()
        # display first few rows
        if display == 'yes':
            current = 0     # current index
            counter = 5     # number of rows to display
            with pd.option_context('display.max_rows', None, 'display.max_columns', None):
                print(df.iloc[current:counter, ])
            current += counter
            while current < df.shape[0]:
                additional = input("Do you want to view additional raw data? Enter yes or no : ").lower()
                if additional == 'yes':
                    # print("current: {}".format(current))
                    # print("counter: {}".format(counter))
                    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
                        print(df.iloc[current:current+counter, ])
                    current += counter
                elif additional == 'no': 
                    break
                else: 
                    print('Invalid Input. Enter one of : yes, no')
            break
        if display == 'no': 
            break
        print('Invalid Input. Enter one of : yes, no')


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        # edit 1 : added display raw data function
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
