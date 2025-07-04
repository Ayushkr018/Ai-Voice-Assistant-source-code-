elif "open tab" in query or "new tab" in query:
          speak("Which website do you want to open?")
          website = takeCommand().lower()

          if ".com" in website or ".co.in" in website or ".org" in website:
            open_new_tab(website, update_conversation)
          else:
           speak("Please say a valid website.")
           update_conversation("Assistant: Invalid website name.")

        elif "close tab" in query:
          speak("How many tabs do you want to close?")
          sleep(1.5)
          number_of_tabs_raw = takeCommand()
    
          if number_of_tabs_raw:
            number_of_tabs = extract_number_from_text(number_of_tabs_raw)
            if number_of_tabs:
             close_tabs(number_of_tabs, update_conversation)
            else:
             speak("Sorry, I didn't understand the number.")
             update_conversation("Assistant: Please say a valid number.")
          else:
            speak("Sorry, I didn't hear anything.")
            update_conversation("Assistant: No input received.")