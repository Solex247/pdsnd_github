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

    # get user's input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
            city = input("Enter a city (Chicago, New york city or Washington): ").lower()
            if city in CITY_DATA:
                break
            else:
                print("Invalid input!. Please input a valid city.")

    # get user input for month (all, january, february, ... , june)

    while True:
        month = input("Enter a month (all or january, february, ..., june): ").lower()
        if month in ['all', 'january', 'february', 'march', 'april', 'may', 'june']:
            break
        else:
            print("Invalid input. Please input a valid month.")


    # get user input for day of week (all, monday, tuesday, ..., sunday)

    while True:
        day = input("Enter a day of the week (all, monday, tuesday, ..., sunday): ").lower()
        if day in ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
            break
        else:
            print("Invalid input. Please input a valid day of the week.")


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

    # Load data file into a DataFrame

    df = pd.read_csv(CITY_DATA[city])

    # Convert the 'Start Time' column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extract month and day of the week from 'Start Time' to create new columns
    df['Month'] = df['Start Time'].dt.month
    df['Day of Week'] = df['Start Time'].dt.day_name()

    # Filter by month if applicable
    if month != 'all':
        month_num = ['january', 'february', 'march', 'april', 'may', 'june'].index(month) + 1
        df = df[df['Month'] == month_num]

    # Filter by day of the week if applicable
    if day != 'all':
        df = df[df['Day of Week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_common_month = df['Month'].mode()[0]
    print("The most common month is:", most_common_month)


    # display the most common day of the week
    most_common_day = df['Day of Week'].mode()[0]
    print("The most common day of the week is: ", most_common_day)


    # display the most common start hour
    df['Hour'] = df['Start Time'].dt.hour
    most_common_start_hour = df['Hour'].mode()[0]
    print("The most common start hour is: ", most_common_start_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]
    print("The most commonly used start station is: ", most_common_start_station)

    # display most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]
    print("The most commonly used end station is: ", most_common_end_station)


    # display most frequent combination of start station and end station trip
    df['Trip'] = df['Start Station'] + ' to ' + df['End Station']
    most_frequent_combination = df['Trip'].mode()[0]
    print(f"The most frequent combination of start station and end station trip is: ", most_frequent_combination)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print(f"Total travel time: {total_travel_time} seconds")


    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print(f"Mean travel time: {mean_travel_time} seconds")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print("Counts of user types:")
    print(user_types)

    # Display counts of gender
    if 'Gender' in df:
        gender_counts = df['Gender'].value_counts()
        print("\nCounts of gender:")
        print(gender_counts)
    else:
        print("\nGender information is not available for this city.")

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        earliest_year_of_birth = int(df['Birth Year'].min())
        most_recent_year_of_birth = int(df['Birth Year'].max())
        common_year_of_birth = int(df['Birth Year'].mode()[0])
        print("\nYear of Birth statistics:")
        print(f"Earliest year of birth: {earliest_year_of_birth}")
        print(f"Most recent year of birth : {most_recent_year_of_birth}")
        print(f"Most common year birth : {common_year_of_birth}")
    else:
        print("\nYear of birth information is not available for this city.")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_data(df):
    show_data = input("Would you like to view 5 rows of individual trip data? Enter yes or no: ").lower()
    start_loc = 0
    chunk_size = 5

    while show_data == 'yes':
        print(df.iloc[start_loc:start_loc + chunk_size])
        view_display = input("Do you wish to continue viewing data? Enter yes or no: ").lower()
        if view_display == 'yes':
            start_loc += chunk_size
            if start_loc < len(df):
                continue
            else:
                print("No more data to display.")
                break
        else:
            break



def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
