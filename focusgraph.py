import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

def focus_graph():
    try:
        with open("focus.txt", "r") as file:
            content = file.readlines()

        if not content:
            print("The 'focus.txt' file is empty.")
            return

        x_dates = []
        y_times = []

        for line in content:
            try:
                # Extract focus time and timestamp from each line
                if "Focus session" in line:
                    focus_time = float(line.split(":")[1].split("hours")[0].strip())  # Extract focus time in hours
                    date_str = line.split("Date:")[1].strip()  # Extract date part

                    session_date = datetime.strptime(date_str, '%Y-%m-%d %H:%M')  # Convert to datetime object
                    x_dates.append(session_date)
                    y_times.append(focus_time)
                else:
                    print(f"Skipping invalid line: {line}")
            except (ValueError, IndexError) as e:
                print(f"Skipping invalid entry: {line} due to {e}")

        if not y_times:
            print("No valid data to plot.")
            return

        # Plotting with dynamic date and time on the x-axis
        plt.figure(figsize=(10, 6))
        plt.plot(x_dates, y_times, color="red", marker="o")

        # Formatting the x-axis to show dates and times clearly
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
        plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=1))  # Set hour interval for clarity
        plt.gcf().autofmt_xdate()  # Rotate date labels for better readability

        # Adding labels and titles dynamically
        plt.title(f"Your Focus Sessions ({len(x_dates)} sessions)", fontsize=16)
        plt.xlabel("Date and Time", fontsize=14)
        plt.ylabel("Focus Time (hours)", fontsize=14)
        plt.grid(True)

        # Save the plot as an image
        plt.savefig("focus_graph.png")
        print("Focus graph saved as 'focus_graph.png'")

        # Show the plot
        plt.show()

    except FileNotFoundError:
        print("The file 'focus.txt' does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Call the function
focus_graph()
