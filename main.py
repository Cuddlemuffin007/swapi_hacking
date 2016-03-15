import requests

choices = {
        'people': {'url': 'http://swapi.co/api/people/', 'key': 'name'},
        'films': {'url': 'http://swapi.co/api/films/', 'key': 'title'},
        'vehicles': {'url': 'http://swapi.co/api/vehicles/', 'key': 'name'}
        }


def get_json_response(url):
    json_response = requests.get(url).json()
    return json_response


def print_all_data_list(url, key):
    base_url = url
    next_url = get_json_response(base_url).get('next')

    print_data_list(get_json_response(base_url), key)
    next_results = input("Press ENTER to see the next page of results or enter 'q' to quit\n>> ")
    if not next_results:
        while next_url:
            if not next_results:
                current_url = next_url
                print_data_list(get_json_response(current_url), key)
                next_results = input("Press ENTER to see the next page of results or enter 'q' to quit\n>> ")
                next_url = get_json_response(current_url).get('next')
            else:
                return None


def print_data_list(json_response, key):
    data = [result.get(key) for result in json_response.get('results')]
    for item in data:
        print(item)


def get_individual_result(url, key, search_string):
    base_url = url
    next_url = get_json_response(base_url).get('next')

    result_list = get_json_response(base_url).get('results')
    while next_url:
        current_url = next_url
        result_list += get_json_response(current_url).get('results')
        next_url = get_json_response(current_url).get('next')

    for result in result_list:
        if result.get(key) == search_string:
            return result
    return None


def print_person_result(result_dict):
    attributes = ['name', 'height', 'mass', 'hair_color', 'skin_color',
            'eye_color', 'birth_year']
    related_attribute_urls = ['species', 'films', 'vehicles', 'starships']
    try:
        for attribute in attributes:
                print("{}: {}".format(attribute, result_dict[attribute]))

        for related_attribute_url in related_attribute_urls:
            print('\n{}:'.format(related_attribute_url.capitalize()))
            for url in result_dict[related_attribute_url]:
                if related_attribute_url == 'films':
                    key = 'title'
                else:
                    key = 'name'
                print(get_json_response(url).get(key))
    except TypeError:
        print("Didn't find what you were looking for?\nRemember, queries are case-sensitive and may contain spaces for full names.")


def print_film_result(result_dict):
    attributes = ['title', 'episode_id', 'opening_crawl', 'director', 'producer', 'release_date']

    try:
        for attribute in attributes:
            print("\n{}: {}".format(attribute, result_dict[attribute]))

        print("\nMain Characters:\n")
        for char_url in result_dict['characters'][0:3]:
            print(get_json_response(char_url).get('name'))
    except TypeError:
        print("Didn't find what you were looking for?\nRemember, queries are case-sensitive and may contain spaces for full names.")


def print_vehicle_result(result_dict):
    attributes = ['name', 'model', 'manufacturer', 'cost_in_credits',
            'length', 'max_atmosphering_speed', 'crew', 'passengers',
            'cargo_capacity', 'consumables', 'vehicle_class']

    try:
        for attribute in attributes:
            print("{}: {}".format(attribute, result_dict[attribute]))
    except TypeError:
        print("Didn't find what you were looking for?\nRemember, queries are case-sensitive and may contain spaces for full names.")


print('\nWelcome to the StarWars API CL project.\n')

while True:

    choice = input("""\nEnter 'people' to list people in Star Wars
Enter 'films' for a list of the Star Wars films
Enter 'vehicles' for a list of vehicles in the Star Wars Universe\n>> """)

    choice_dict = choices.get(choice)
    if choice_dict:
        url = choice_dict.get('url')
        key = choice_dict.get('key')

        if choice == 'people':
            name = input("If you would like to search for a specific person, enter their full name now. Or press ENTER to see a list of all people.\n>> ")
            if name:
                result = get_individual_result(url, key, name)
                print_person_result(result)
            else:
                json_response = get_json_response(url)
                print_all_data_list(url, key)
        elif choice == 'vehicles':
            vehicle_name = input("If you would like to search for a specific vehicle, enter the name now. Press ENTER for list view.\n>> ")
            if vehicle_name:
                result = get_individual_result(url, key, vehicle_name)
                print_vehicle_result(result)
            else:
                json_response = get_json_response(url)
                print_data_list(json_response, key)
        elif choice == 'films':
            film_title = input("If you'd like to search for a specific movie, enter the title now. Press ENTER for list view.\n>> ")
            if film_title:
                result = get_individual_result(url, key, film_title)
                print_film_result(result)
            else:
                json_response = get_json_response(url)
                print_data_list(json_response, key)
    else:
        print('Please enter a valid choice')
        continue

