import requests

def search_location(query:str)->list[dict]:
    """
    Search for a location using the OpenStreetMap API.

    Args:
        query (str): The search query for the desired location.

    Returns:
        list: A list of dictionaries containing location data in JSON format if the request is successful.
        None: Returns None if the request fails or an error occurs.

    Example
        location_data = search_location("Irvine, CA")
        if location_data:
            print(location_data[0])  #Prints the first result
    """

    #Base URL for API
    url = "https://nominatim.openstreetmap.org/search"

    # Query parameters
    params = {
        "q": query,      
        "format": "json"
    }

    # Add a proper User-Agent to avoid being blocked
    headers = {
        "User-Agent": "StreetAPI/1.0 (gerberj1@uci.edu)" 
    }

    #Request to get response
    response = requests.get(url, params=params, headers=headers)

    #Checking response
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error {response.status_code}: {response.text}")
        return None

