#Canadian Inflation Calculator

import pandas as pd
import numpy as np

#Create a class called InflationCalculator
class InflationCalculator:
    #Constructor initalizes the object with the CPI data file
    def __init__(self, filename):
        #Read the CPI data
        # #header=8 tells pandas that the column headings are on row 9
        # #since the first 8 rows contain information about the dataset
        self.cpi_data = pd.read_csv(filename, header=8)

    #Method to check if a date is vaild and exists in the CPI data
    def check_date(self, date):
        #Check that the date follows the YYYY-MM format
        if len(date) != 7 or date[4] != "-":
            return False
        #Check that the year and month contain only numbers
        if not date[:4].isdigit() or not date[5:].isdigit():
            return False
        #Check that the month is between 1 and 12
        month = int(date[5:])
        if month < 1 or month > 12:
            return False
        #Add the first day of the month to match the CSV file
        full_date = date + "-01"
        #Find the matching date in the CPI data
        matching_date = self.cpi_data[
            self.cpi_data["date"] == full_date
        ]
        #Return True if the date exists in the dataset
        if len(matching_date) > 0:
            return True
        else:
            return False

    #Method to find the CPI value for the selected date
    def get_cpi(self, date):
        #Add the first day of the month to match the CSV file
        full_date = date + "-01"
        #Find the row containing the selected date
        matching_date = self.cpi_data[
            self.cpi_data["date"] == full_date
        ]
        #Get the CPI value from the matching row
        cpi = matching_date["STATIC_INFLATIONCALC"].iloc[0]
        #Return the CPI value
        return cpi

    #Method the calculate the inflation-adjusted price
    def calculate(self, price, date1, date2):
        #Get the CPI values for both dates
        cpi1 = self.get_cpi(date1)
        cpi2 = self.get_cpi(date2)
        #Store both CPI values in the numpy array
        cpi_values = np.array([cpi1, cpi2])
        #Calculate the adjusted price using the CPI values
        adjusted_price = price * (cpi_values[1] / cpi_values[0])
        #Calculate the percentage change in CPI
        percentage_change = ((cpi_values[1] / cpi_values[0]) - 1) * 100
        #Extract the year and month from the first date
        year1 = int(date1[:4])
        month1 = int(date1[5:])
        #Extract the year and month from the second date
        year2 = int(date2[:4])
        month2 = int(date2[5:])
        #Calculate the number of months between the dates
        months = (year2 - year1) * 12 + (month2 - month1)
        #Convert the time difference into years
        years = abs(months) / 12
        #Calculate the annualized inflation rate
        #If the dates are the same, the rate is zero
        if months == 0:
            annual_rate = 0
        else:
            #Use compound growth to calculate annual inflation
            annual_rate = (
                (cpi_values[1] / cpi_values[0]) ** (12 / months) - 1
            ) * 100
        #Return all calculated results
        return adjusted_price, percentage_change, years, annual_rate, cpi1, cpi2

#Main program
if __name__ == "__main__":
    #Welcome message
    print("Welcome to the Canadian Inflation Calculator!")
    #Create an InflationCalculator object using the CPI file
    calculator = InflationCalculator("STATIC_INFLATIONCALC.csv")
    #Ask the user to enter the original price
    #Keep asking until a valid price is entered
    while True:
        try:
            price = float(input("Enter the original price: $"))
            #Check that the price is valid and not negative
            if price >= 0 and price < float("inf"):
                break
            else:
                print("Invalid price. Please enter a positive number.")
        #Display an error if the user enters text instead of a number
        except ValueError:
            print("Invalid price. Please enter a number.")
    #Ask the user to enter the first date
    while True:
        date1 = input("Enter the first date (YYYY-MM): ")
        #Check if the date is valid
        if calculator.check_date(date1):
            break
        else:
            print("Invalid date. Please enter a date available in the CPI data.")
    #Ask the user to enter the second date
    while True:
        date2 = input("Enter the second date (YYYY-MM): ")
        #Check if the date is valid
        if calculator.check_date(date2):
            break
        else:
            print("Invalid date. Please enter a date available in the CPI data.")
    #Calculate inflation using the entered price and dates
    adjusted_price, percentage_change, years, annual_rate, cpi1, cpi2 = calculator.calculate(
        price, date1, date2
    )

    #Display the results
    print("\nInflation Calculator Results")
    print(30 * "-")

    #Display the original price and date
    print("A basket of goods and services")
    print("That cost: ${:,.2f} CAD in {}".format(price, date1))
          
    #Display the adjusted price and comparison date
    print("Would cost: ${:,.2f} CAD in {}".format(adjusted_price, date2))

    print(30 * "-")

    #Display the percentage change in prices
    print("Percentage Change: {:.2f}%".format(percentage_change))

    #Display the time difference in years
    print("Number of Years: {:.2f}".format(years))

    #Display the annualized inflation rate
    print("Average Annual Rate of Inflation: {:.2f}%".format(annual_rate))

    #Display the CPI values
    print("CPI for First Date: {:.2f}".format(cpi1))
    print("CPI for Second Date: {:.2f}".format(cpi2))

    print(30 * "-")
    print("2002 CPI = 100.0")