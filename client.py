import requests
import time

def register_user(username, password, base_url="http://localhost:8000"):
    """
    Registers a new user by making a POST request to the /register endpoint.

    Args:
        username (str): The username to register.
        password (str): The password for the user.
        base_url (str): The base URL of the API.

    Returns:
        dict: The JSON response from the server if the request is successful.
    """
    url = f"{base_url}/register"
    user_data = {"username": username, "password": password}
    
    try:
        response = requests.post(url, json=user_data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        # Handle 400 error for existing user gracefully
        if response.status_code == 400:
            print("User may already exist.")
        else:
            print(f"Response body: {response.text}")
        return None
    except requests.exceptions.RequestException as err:
        print(f"An error occurred: {err}")
        return None

def login(username, password, base_url="http://localhost:8000"):
    """
    Logs in a user to get a JWT token.

    Args:
        username (str): The username to log in with.
        password (str): The password for the user.
        base_url (str): The base URL of the API.

    Returns:
        str: The access token if login is successful, otherwise None.
    """
    url = f"{base_url}/login"
    login_data = {"username": username, "password": password}
    
    try:
        response = requests.post(url, data=login_data)
        response.raise_for_status()
        return response.json().get("access_token")
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred during login: {http_err}")
        print(f"Response body: {response.text}")
        return None
    except requests.exceptions.RequestException as err:
        print(f"An error occurred during login: {err}")
        return None

def create_poll(question, options, token, base_url="http://localhost:8000"):
    """
    Creates a new poll. Requires authentication.

    Args:
        question (str): The question for the poll.
        options (list): A list of strings for the poll options.
        token (str): The JWT access token for authentication.
        base_url (str): The base URL of the API.

    Returns:
        dict: The created poll object, or None if an error occurs.
    """
    url = f"{base_url}/polls"
    headers = {"Authorization": f"Bearer {token}"}
    poll_data = {"question": question, "options": options}
    
    try:
        response = requests.post(url, json=poll_data, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred while creating poll: {http_err}")
        print(f"Response body: {response.text}")
        return None
    except requests.exceptions.RequestException as err:
        print(f"An error occurred while creating poll: {err}")
        return None

def cast_vote(poll_id, option_id, token, base_url="http://localhost:8000"):
    """
    Casts a vote on a specific poll. Requires authentication.

    Args:
        poll_id (int): The ID of the poll to vote on.
        option_id (int): The ID of the option to vote for.
        token (str): The JWT access token for authentication.
        base_url (str): The base URL of the API.

    Returns:
        dict: The result of the vote, or None if an error occurs.
    """
    url = f"{base_url}/polls/{poll_id}/vote"
    headers = {"Authorization": f"Bearer {token}"}
    vote_data = {"option_id": option_id}
    
    try:
        response = requests.post(url, json=vote_data, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred while casting vote: {http_err}")
        print(f"Response body: {response.text}")
        return None
    except requests.exceptions.RequestException as err:
        print(f"An error occurred while casting vote: {err}")
        return None

def get_poll_results(poll_id, base_url="http://localhost:8000"):
    """
    Retrieves the results for a specific poll.

    Args:
        poll_id (int): The ID of the poll.
        base_url (str): The base URL of the API.

    Returns:
        dict: The poll results, or None if an error occurs.
    """
    url = f"{base_url}/polls/{poll_id}/results"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred while getting poll results: {http_err}")
        print(f"Response body: {response.text}")
        return None
    except requests.exceptions.RequestException as err:
        print(f"An error occurred while getting poll results: {err}")
        return None


if __name__ == "__main__":
    # It's good practice to have a base URL configuration
    BASE_URL = "http://localhost:8000"

    # --- User Registration and Login ---
    # To avoid issues with re-running, let's use a unique username each time
    unique_username = f"testuser_{int(time.time())}"
    print(f"Registering a new user: {unique_username}...")
    
    # Use a try-except block to handle potential registration failures
    try:
        registered_user = register_user(unique_username, "testpassword", base_url=BASE_URL)
        if not registered_user:
            raise Exception("Registration failed.")
        print("Registered user:", registered_user)

        # --- Login to get token ---
        print("Logging in...")
        token = login(unique_username, "testpassword", base_url=BASE_URL)
        if not token:
            raise Exception("Login failed.")
        print("Login successful. Token received.")

        # --- Create a new poll ---
        print("Creating a new poll...")
        poll_data = {
            "question": "What is your favorite programming language?",
            "options": ["Python", "JavaScript", "Go", "Rust"]
        }
        created_poll = create_poll(poll_data["question"], poll_data["options"], token, base_url=BASE_URL)
        if not created_poll:
            raise Exception("Poll creation failed.")
        print("Poll created:", created_poll)
        
        poll_id = created_poll.get("id")
        if not poll_id:
            raise Exception("Could not get poll ID from created poll.")

        # --- Cast a vote ---
        # Let's assume the user wants to vote for the first option.
        # In a real app, you'd get the option ID from the created_poll object.
        # For simplicity, we'll assume option IDs start at 1 and increment.
        option_id_to_vote = created_poll['options'][0]['id']
        print(f"Casting a vote for option {option_id_to_vote} in poll {poll_id}...")
        vote_result = cast_vote(poll_id, option_id_to_vote, token, base_url=BASE_URL)
        if not vote_result:
            raise Exception("Failed to cast vote.")
        print("Vote cast successfully:", vote_result)

        # --- Get Poll Results ---
        print(f"Retrieving results for poll {poll_id}...")
        poll_results = get_poll_results(poll_id, base_url=BASE_URL)
        if not poll_results:
            raise Exception("Failed to get poll results.")
        print("Poll results:", poll_results)

    except Exception as e:
        print(f"An error occurred during the client test run: {e}")

