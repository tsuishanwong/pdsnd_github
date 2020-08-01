import time
import pandas as pd
import numpy as np
import datetime

pd.set_option('display.max_colwidth', -1)

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyse from, where the cities available are chicago, new york city and washington
        (str) month - name of the month to filter by (january - june), or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # Ask for user input for city (chicago, new york city, washington).
    while True:
        city = input('\nChoose from chicago, new york city or washington: ').lower()
        if city in ('chicago','new york city','washington'):
            break
        else:
            print('Sorry that\'s not from the list.\nPlease try again.')

    # Ask for user input for month (all, january, february, ... , june)
    while True:
        month = input("\nEnter a month OR all for no filtering. Available months: january - june: ").lower()
        if month in ('all','january','february','march','april','may','june'):
            break
        else:
            print('Sorry that\'s not a month from the list. No abbreviations allowed.\nPlease try again.')

    # Ask for user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input('\nEnter a weekday OR all for no filtering: ').lower()
        if day in ('all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'):
            break
        else:
            print('This is not a valid weekday name.\nPlease try again.')

    print("\nYou have chosen to look at:\nCity: {}\nMonth: {}\nWeekday: {}".format(city.title(),month.title(),day.title()))
    print('-'*40)
    return city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyse; chicago, new york city or washington.
        (str) month - name of the month to filter by (january - june), or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])

    # Convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # Filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df

def time_stats(df):
    """
    Displays statistics on the most frequent times of travel.

    Returns for the selected city, month and weekday the most popular month/weekday/hour to travel

    """

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Calculates the most common month
    popular_month = df['month'].mode().to_string(index=False)
    datetime_object = datetime.datetime.strptime(popular_month, "%m")
    popular_month_name = datetime_object.strftime("%B")
    print("The most popular month to travel is: {}".format(popular_month_name))

    # Calcuates the most common day of week
    popular_day = df['day_of_week'].mode().to_string(index=False)
    print("The most popular day of the week for travel is: {}".format(popular_day))

    # Calculates the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode().to_string(index=False)
    print("The most popular hour for travel is: {}".format(popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    print('The most popular...')

    # Calculates the most commonly used start station
    popular_start = df['Start Station'].mode().to_string(index=False)
    print("Start station is: {}.".format(popular_start))

    # Calculates the most commonly used end station
    popular_end = df['End Station'].mode().to_string(index=False)
    print("End station is: {}.".format(popular_end))

    # Calculates the most frequent combination of start station and end station trip
    df['Trip'] = 'Starts at: ' + df['Start Station'] + '$Ends at: ' + df['End Station']
    popular_trip = df['Trip'].mode().to_string(index=False)
    print("\nThe most frequently used trip\n{}\n{}.".format(popular_trip.split('$')[0],popular_trip.split('$')[1]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    days_in_seconds = 86400
    hours_in_seconds = 3600
    mins_in_seconds = 60

    # Calcaultes the total travel time
    total_time = df['Trip Duration'].sum()
    days = total_time // days_in_seconds
    hours = (total_time - days*days_in_seconds) // hours_in_seconds
    mins = (total_time - days*days_in_seconds - hours*hours_in_seconds) // mins_in_seconds
    secs = total_time - days*days_in_seconds - hours*hours_in_seconds - mins*mins_in_seconds
    print("The sum of all trip durations is: {} days, {} hours, {} minutes, and {} seconds (Total {} seconds).".format(int(days),int(hours),int(mins),round(secs,2),total_time))

    # Calcaultes the average travel time
    mean_time = df['Trip Duration'].mean()
    mean_hours = mean_time // hours_in_seconds
    mean_mins = (mean_time - mean_hours*hours_in_seconds) // mins_in_seconds
    mean_secs = mean_time - mean_hours*hours_in_seconds - mean_mins*mins_in_seconds
    print("The average trip duration per user is: {} hours, {} minutes, and {} seconds ( Total {} seconds).".format(int(mean_hours),int(mean_mins),round(mean_secs,2),mean_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Calculates counts of user types
    print("User Type Count:")
    print(df['User Type'].value_counts().to_string())

    # Calculates counts of gender
    print("\nGender Count:")
    try:
        print(df['Gender'].value_counts().to_string())
    except KeyError:
        print("Gender information not available for this city.")


    # Calculates the earliest, most recent, and most common year of birth
    print("\nYear of Birth Stats:")
    try:
        print("Earliest Birth Year: ",int(df['Birth Year'].min()))
        print("Most Recent Birth Year: ",int(df['Birth Year'].max()))
        print("Most Common Birth Year: ",df['Birth Year'].mode().to_string(index=False)[:-2])
    except:
        print("No Year of birth stats available for this city.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        # Ask if the user would like to see the first 5 lines of data, shifting down 5 each time they say yes
        user_count = 0
        while True:
            show_data = input('\nWould you like to see some of the data? Please type yes or no: ')
            if show_data.lower() == 'yes':
                df1 = df[user_count:]
                if user_count == 0:

                    print('Here is the first 5 lines of data:\n')
                else:
                    print('Here is the next 5 lines of data:\n')
                print(df1.head())
                user_count+=5
                df1 = df1.iloc[user_count:]
            else:
                break

        # Prints out the most popular travel times to the user if they select yes
        time_stat_q = input('\nAre you interested in the most popular times of travel? Please enter yes or no: ')
        if time_stat_q.lower() == 'yes':
            time_stats(df)
        else:
            print('Skipping time stats.')

        # Prints out the most popular stations to the user if they select yes
        station_stat_q = input('\nWould you like to find out the most popular stations? Please enter yes or no: ')
        if station_stat_q.lower() == 'yes':
            station_stats(df)
        else:
            print('Skipping stations stats.')

        # Prints out the trip duration stats if user selects yes
        trip_duration_stat_q = input('\nTrip duration stats are available, are you interested? Please enter yes or no: ')
        if trip_duration_stat_q.lower() == 'yes':
            trip_duration_stats(df)
        else:
            print('Skipping trip duration stats.')

        # Prints bikeshare user stats if user has typed in yes
        user_stat_q = input('\nFind out more about the bikeshare users by selecting yes. If you would like to skip, type no: ')
        if user_stat_q.lower() == 'yes':
            user_stats(df)
        else:
            print('Skipping user stats.')

        # Asks users if they would like to repeat the exercise
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
