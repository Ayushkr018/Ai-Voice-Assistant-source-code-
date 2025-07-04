import tkinter as tk
from time import strftime
import turtle
import threading

def start_gui(activate_voice_assistant):
    """Function to initialize the GUI for the voice assistant."""
    global window, conversation_text, time_label, mic_button, turtle_screen, turtle_glow

    window = tk.Tk()
    window.title("Ellyse: your Virtual Ace")
    window.geometry("600x600")
    window.config(bg="#121212")

    title_label = tk.Label(window, text="Ellyse: Your Virtual Ace", font=("Helvetica", 20, "bold"), fg="cyan", bg="#00008B")
    title_label.pack(pady=10)

    mic_frame = tk.Frame(window, bg="#121212")
    mic_frame.pack(pady=10)

    turtle_canvas = tk.Canvas(mic_frame, width=200, height=200, bg="#121212", highlightthickness=0)
    turtle_canvas.pack()

    turtle_screen = turtle.TurtleScreen(turtle_canvas)
    turtle_screen.bgcolor("#121212")
    turtle_screen.tracer(0)

    turtle_glow = turtle.RawTurtle(turtle_screen)
    turtle_glow.shape("circle")
    turtle_glow.color("#FF0000")
    turtle_glow.penup()

    def turtle_glow_animation(radius=3.0, delta=0.2, min_radius=1.5, max_radius=4.0):
        turtle_glow.shapesize(radius)  
        radius += delta
        if radius >= max_radius or radius <= min_radius:
            delta = -delta  

        turtle_screen.update()  
        window.after(70, turtle_glow_animation, radius, delta, min_radius, max_radius)

    def update_conversation(text):
        """Update conversation in the GUI's conversation Text widget."""
        conversation_text.insert(tk.END, text + "\n")  # Insert the new text at the end
        conversation_text.see(tk.END)  # Automatically scroll to the end to show the latest message

    # Function to start the Turtle glow effect
    def button_glow_effect():
        turtle_glow_animation()  # Start the glow animation with Turtle

    # Voice assistant activation function (called when the button is pressed)
    def activate_voice():
        conversation_text.delete(1.0, tk.END)  # Clear previous conversation
        update_conversation("User: Activating voice assistant...")
        button_glow_effect()  # Start the button glow effect (continuous)

        # Run the voice assistant in a separate thread to prevent GUI freezing
        def run_voice_assistant():
            result = activate_voice_assistant(update_conversation)  # Start assistant, pass conversation updates
            if result == "close":
                window.destroy()  # Close the window

        # Start the thread for the voice assistant
        threading.Thread(target=run_voice_assistant, daemon=True).start()

    # Button to activate voice assistant (inside mic_frame)
    mic_button = tk.Button(mic_frame, text="Tap to Start", font=("Helvetica", 14), command=activate_voice, bg="#ff5050", fg="black", relief="raised", bd=3)
    mic_button.pack(pady=10)

    # Conversation frame (separate from the mic button)
    conversation_frame = tk.Frame(window, bg="#1f1f1f", width=400, height=250)
    conversation_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    # Add a scrollable Text widget for conversation display
    conversation_text = tk.Text(conversation_frame, font=("Helvetica", 12, "bold"), fg="cyan", bg="#1f1f1f", 
                                wrap=tk.WORD, height=10)
    conversation_text.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

    # Add Scrollbar
    scrollbar = tk.Scrollbar(conversation_frame, command=conversation_text.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    conversation_text.config(yscrollcommand=scrollbar.set)

    # Frame for time, day, and date at the bottom
    bottom_frame = tk.Frame(window, bg="#121212")
    bottom_frame.pack(side=tk.BOTTOM, pady=10)

    # Time label with time, day, and date on separate lines
    time_label = tk.Label(bottom_frame, font=("Helvetica", 14, "bold"), fg="cyan", bg="#121212")
    time_label.pack()

    # Display current time, day, and date in separate lines
    def time_display():
        time_string = strftime('%H:%M:%S %p')
        day_string = strftime('%A')
        date_string = strftime('%d %B %Y')

        # Display in separate lines with the newlines added
        time_label.config(text=f"{time_string}\n{day_string}\n{date_string}")
        window.after(1000, time_display)  # Update every second

    # Start displaying the time, day, and date
    time_display()

    # Start the main loop
    window.mainloop()