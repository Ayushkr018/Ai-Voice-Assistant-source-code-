import matplotlib.pyplot as plt

def focus_graph():
    focus_times = []
    total_focus_time = 0

    # Open the focus log file
    with open('focus_log.txt', 'r') as file:
        lines = file.readlines()

    for line in lines:
        try:
            if "Focus session" in line:
                # Extract the focus time (assuming hours is used in the log)
                focus_time = float(line.split(":")[1].split()[0])
                focus_times.append(focus_time)
                total_focus_time += focus_time
            elif "Total focus time" in line:
                print(line.strip())  # For debug purposes
        except (IndexError, ValueError):
            print(f"Skipping invalid line: {line.strip()}")

    if focus_times:
        plt.figure(figsize=(8, 6))
        plt.plot(focus_times, marker='o', linestyle='-', color='b', label="Focus Sessions")
        plt.title('Focus Time Per Session')
        plt.xlabel('Session Number')
        plt.ylabel('Time (hours)')
        plt.legend()
        plt.grid(True)
        plt.savefig('focus_graph.png')
        plt.close()

        print(f"Focus graph saved as 'focus_graph.png'")
    else:
        print("No valid focus data found.")

