import pygame
import sys
import hashlib
import numpy as np
import os
# Define global variables
import maze_game

# database primary key stuff
import uuid


login_display = pygame.display.set_mode((800, 600))
# Initialize pygame and set up the display
pygame.init()
# Set the window title
pygame.display.set_caption("LOST - Login")

# button implamented from the maze_game.py
def buttonforlogin(login_display, pos, text):
    # Define button dimensions
    font = pygame.font.Font('Kenney Future Narrow.ttf', 30)
    text_render = font.render(text, True, (255, 255, 255))
    x, y, w, h = text_render.get_rect()
    x, y = pos
    w = w + 10
    h = h + 10
    text_x = x + (w - text_render.get_width()) // 2
    text_y = y + (h - text_render.get_height()) // 2
    # Create button Rect object and draw button
    pygame.draw.line(login_display, (134, 202, 234), (x, y), (x + w, y), 5)  # top
    pygame.draw.line(login_display, (134, 202, 234), (x, y - 2), (x, y + h), 5)  # left
    pygame.draw.line(login_display, (28, 115, 156), (x, y + h), (x + w, y + h), 5)  # right
    pygame.draw.line(login_display, (28, 115, 156), (x + w, y + h), [x + w, y], 5)  # bottom
    pygame.draw.rect(login_display, (37, 154, 208), (x, y, w, h))  # fill
    return login_display.blit(text_render, (text_x, text_y))

def login_screen_fun():
    if not os.path.isfile("users_info.npy"):
        create_user_file("userID", "username", "hashed_password")
    # Load fonts and create text surfaces
    fontL = pygame.font.Font('Kenney Future Narrow.ttf', 150)
    fontM = pygame.font.Font('Kenney Future Narrow.ttf', 30)
    fontX = pygame.font.SysFont('Arial Bold', 40)
    # Create login form elements
    username_input = pygame.Rect(250, 200, 300, 50)
    password_input = pygame.Rect(250, 300, 300, 50)
    # Create text for login elements
    username_text = fontM.render("Username", True, (0, 0, 0))
    password_text = fontM.render("Password", True, (0, 0, 0))
    # title
    title_text = fontL.render("LOST", True, (0, 0, 0))
    # boxes start off empty
    username_entry = ""
    password_entry = ""
    # creating buttons for login and signup using the function very similar to the one in maze_game.py changed
    login_button = buttonforlogin(login_display, (350, 400), "Log In")
    signup_button = buttonforlogin(login_display, (350, 475), "Sign Up")
    # when no box is clicked, no box is selected
    active_input = None

    # Start the login login_display loop
    while True:
        for event in pygame.event.get():
            # Quit if the quit button was pressed
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                # Check for backspace press in username/input box
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    if active_input == 'username':
                        username_entry = username_entry[:-1]
                    elif active_input == 'password':
                        password_entry = password_entry[:-1]
                        # Check for letter keypress in username input box

                if event.key == pygame.K_RETURN:
                    if active_input == 'username':
                        active_input = 'password'
                    elif active_input == 'password':
                        if validate(login_display, username_entry, password_entry):
                            login_button_press(login_display, username_entry, password_entry)

                if event.key == pygame.K_TAB:
                    if active_input == 'username':
                        active_input = 'password'
                    elif active_input == 'password':
                        active_input = 'username'

                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

                else:
                    if active_input == 'username':
                        if event.unicode.isalnum():
                            username_entry += event.unicode
                    elif active_input == 'password':
                        if event.unicode.isalnum():
                            password_entry += event.unicode

            # Check for mouse click in username input box and selects the box that is clicked
            if event.type == pygame.MOUSEBUTTONDOWN:
                if username_input.collidepoint(event.pos):
                    active_input = 'username'
                elif password_input.collidepoint(event.pos):
                    active_input = 'password'
                else:
                    # when no box is clicked, no box is selected
                    active_input = None

                    # what to do if login is clicked
                if login_button.collidepoint(event.pos):
                    print("Log in clicked")
                    if validate(login_display, username_entry, password_entry):
                        login_button_press(login_display, username_entry, password_entry)
                        # what to do if login is clicked

                elif signup_button.collidepoint(event.pos):
                    print("Sign up clicked")
                    if validate(login_display, username_entry, password_entry):
                        signup_attempt(login_display, username_entry, password_entry)
                        # what to do if login is clicked

        # Clear the login_display
        login_display.fill((255, 133, 194))

        # Draw login form elements
        pygame.draw.rect(login_display, (0, 0, 0), username_input, 2)
        pygame.draw.rect(login_display, (0, 0, 0), password_input, 2)
        # Render text login box "titles" for username
        login_display.blit(username_text, (80, 210))
        login_display.blit(password_text, (80, 310))
        # Render text for for username
        username_entry_text = fontX.render(username_entry, True, (0, 0, 0))
        # Render text for password in ***** format
        password_entry_text = fontM.render("*" * len(password_entry), True, (0, 0, 0))
        # Blit username and password text surfaces to the login_display in the center of their respective boxes
        login_display.blit(username_entry_text, (username_input.x + 10, username_input.y + 15))
        login_display.blit(password_entry_text, (password_input.x + 10, password_input.y + 15))
        # Render title text "lost"
        login_display.blit(title_text, (225, 20))
        # adds the login and signup buttons which are connected to their respective functions below
        login_button = buttonforlogin(login_display, (350, 400), "Log In")
        signup_button = buttonforlogin(login_display, (350, 475), "Sign Up")
        # Update the login_display
        pygame.display.update()


# function that will prevent the user from submitting blank username and password and will check if the
# username and password match the ones in the database by sending them to signup_attempt function
def validate(login_display, username_entry, password_entry):
    username = username_entry
    password = password_entry

    # check if username and password are less than 14 characters and are alphanumeric and not blank
    if not username or not password:
        message(login_display, "Error: Username and password cannot be blank")
        return False
    elif len(username) > 13 or len(password) > 13:
        message(login_display, "Error: Username and password must be 14 characters or less")
        return False
    elif not username.isalnum() or not password.isalnum():
        message(login_display, "Error: Username and password must be alphanumeric only")
        return False
    else:
        return True

# function tha will write a new user to the database if the username is
# not already taken and the username and password are not blank (password hashed before storing)
def signup_attempt(login_display, username, password):
    # Check if username is already taken
    if os.path.isfile("users_info.npy"):
        users = np.load("users_info.npy", allow_pickle=True).tolist()
    else:
        users = {}

    if any(user["username"] == username for user in users.values()):
        message(login_display, "Error: Username already taken")
        return False

    # Hash the password and add the new user to the dictionary encodes with utf-8 and converts to hexadecimal
    hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
    password = ""
    # generate a random user id for the new user
    user_id = str(uuid.uuid4())
    users[user_id] = {"username": username, "hashed_password": hashed_password, "high_score": 86400}

    # Save the updated dictionary to file
    np.save("users_info.npy", users)

    message(login_display, "User successfully signed up")
    return True

# function to display messages based on different inputs e.g. successful login, incorrect password etc.
def message(login_display, message):
    font = pygame.font.SysFont('Lucida Console', 30)
    text = font.render(message, True, (255, 0, 0))
    # create a rectangle to serve as the background for the message, centered on the login_display too
    text_rect = text.get_rect(center=(800 // 2, 600 // 2))

    # create a rectangle to serve as the background for the message
    background_rect = text.get_rect()
    # inflate the rectangle to create a border around the message
    background_rect.inflate_ip(10, 10)
    # center the rectangle on the login_display
    background_rect.center = login_display.get_rect().center

    # draw the background rectangle and message surface onto the login_display
    pygame.draw.rect(login_display, (0, 0, 0), background_rect)
    login_display.blit(text, text.get_rect(center=login_display.get_rect().center))
    # draw the background rectangle and message surface onto the login_display
    login_display.blit(text, text_rect)
    pygame.display.update()
    # message displayed for 1.5 seconds
    pygame.time.delay(1500)

# function connected to login button to check if username and password
# are in data base and match each other (password is hashed before being stored)
def login_attempt(login_display, username_entry, password_entry):
    # Check if user exists and password is correct
    filename = "users_info.npy"
    # Check if the file exists
    if os.path.isfile(filename):
        # Load the existing user data
        users_database = np.load(filename, allow_pickle=True).item()
        if isinstance(users_database, dict):
            # The data is a dictionary (expected)
            pass
        else:
            # The data is not a dictionary, return an error message
            message(login_display, "Error: Failed to load user data")
            return False

        # Loop through the users and check if the username matches
        for user_id, user_data in users_database.items():
            # Check if the username matches
            if user_data["username"] == username_entry:
                # hashes pass
                hashed_password = hashlib.sha256(password_entry.encode('utf-8')).hexdigest()
                password_entry = ""
                # Check if the password matches
                if user_data["hashed_password"] == hashed_password:
                    # If we get here, the login was successful
                    message(login_display, "Login successful")
                    # launch the game
                    theApp = maze_game.Window(user_id)
                    theApp.execute()
                    pygame.quit()
                    return True
    else:
        message(login_display, "Error: User data file not found")
        return False

#preventing brute force attacks by limiting the number of login attempts to 5
counter = 0
def login_button_press(login_display, username_entry, password_entry):
    global counter
    if login_attempt(login_display, username_entry, password_entry):
        True
    else:
        message(login_display, "Invalid login details.")
        counter += 1
        if counter == 5:
            message(login_display, "Too many login attempts. EXITING.")
            exit()

# function to create a new user file if one does not already exist
def create_user_file(userID, username, hashed_password):
    file_name = 'users_info.npy'

    if os.path.isfile(file_name):
        # load the existing user data
        users_record = np.load(file_name, allow_pickle=True)
        user_dict = users_record.item()
    else:
        # create a new user data dictionary if the file doesn't exist
        user_dict = {}

    # create a dictionary for the new user
    new_user_dict = {'username': username, 'hashed_password': hashed_password, 'high_score': 86400}

    # add the new user to the user data dictionary
    user_dict[userID] = new_user_dict

    # save the updated user data dictionary to the file
    np.save(file_name, user_dict)


login_screen_fun()
