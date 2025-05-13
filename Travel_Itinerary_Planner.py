import pandas as pd
from geopy.geocoders import Nominatim
import math
import zipfile
import requests
from tabulate import tabulate 

def get_coordinates(location):
    """Get latitude and longitude of a location using OpenStreetMap's Nominatim."""
    geolocator = Nominatim(user_agent="distance_calculator")
    location_data = geolocator.geocode(location)
    if location_data:
        return location_data.latitude, location_data.longitude
    else:
        print(f"Could not find location: {location}")
        return None

def haversine(lat1, lon1, lat2, lon2):
    """Calculate the great-circle distance between two coordinates using the Haversine formula."""
    R = 6371  # Earth radius in km
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c  # Distance in km

def insertdetails():
    """This function will ask the user for location details and return them."""
    current_location = input("\nEnter your current location : ")
    destination = input("Enter Destination: ").strip().capitalize()
    return current_location, destination

def hotel():
    global s, day, c, total_food_cost, n_people, dish
    n_people = int(input("Enter the number of people: "))
    day = int(input("\nEnter the Number of days: "))
    stay = int(input("1.Luxury Hotel(₹5000/day)\n2.Midrange Hotel(₹2000/day)\n3.Budget Hotel(₹1000/day)\nEnter your choice: "))
    
    if stay == 1:
        c = day * 5000 * n_people
        s = "Luxury Hotel"
        print(f"\nThe total cost for {day} days for {n_people} people is ₹{c}")
        food_prices = {"Breakfast": 150, "Lunch": 400, "Dinner": 500}
    elif stay == 2:
        c = day * 2000 * n_people
        s = "Midrange Hotel"
        print(f"\nThe total cost for {day} days for {n_people} people is ₹{c}")
        food_prices = {"Breakfast": 100, "Lunch": 250, "Dinner": 300}
    elif stay == 3:
        c = day * 1000 * n_people
        s = "Budget Hotel"
        print(f"\nThe total cost for {day} days for {n_people} people is ₹{c}")
        food_prices = {"Breakfast": 70, "Lunch": 150, "Dinner": 200}
    else:
        print("Invalid Choice!")
        return 0, "", 0, 0

    total_food_cost = 0
    for i in range(1, day + 1):
        print(f"\nDay {i} Meal Selection:")
        more = 1
        while more == 1:
            dishes = int(input("\nWhich food do you prefer?\n1. Indian Food\n2. Italian Food\n3. Chinese Food\nEnter your choice: "))
            if dishes == 1:
                dish = "Indian Food"
            elif dishes == 2:
                dish = "Italian Food"
            elif dishes == 3:
                dish = "Chinese Food"
            else:
                print("Invalid Choice!")
                continue

            food = int(input("1. Breakfast\n2. Lunch\n3. Dinner\nEnter your choice: "))
            if food == 1:
                f = "Breakfast"
                price = food_prices["Breakfast"]
            elif food == 2:
                f = "Lunch"
                price = food_prices["Lunch"]
            elif food == 3:
                f = "Dinner"
                price = food_prices["Dinner"]
            else:
                print("Invalid Choice!")
                continue

            daily_food_cost = price * n_people
            total_food_cost += daily_food_cost
            
            print(f"Added {f} for {n_people} people: ₹{daily_food_cost}")
            more = int(input("Add another meal for this day? (1=Yes/0=No): "))

    print(f"\nTotal food cost for {n_people} people for {day} days: ₹{total_food_cost}")
    return c, s, day, total_food_cost

def activities(destination, day):
    """Let user select activities for each day of their trip."""
    file_path = r"C:\Users\hrushikesh thombare\OneDrive\Desktop\Zip files\indian_cities_travel_data.csv"
    df = pd.read_csv(file_path)
    
    if destination not in df["City"].values:
        print("Sorry, we don't have data for that city.")
        return {}

    activity_types = {
        1: "Famous Shopping Places",
        2: "Relaxation Spots", 
        3: "Hiking/Trekking Spots"
    }

    daily_activities = {}  # {day1: [activity1, activity2], day2: [...]}

    for day_num in range(1, day + 1):
        print(f"\nDay {day_num} Activities:")
        print("Choose activity type:")
        print("1. Famous Shopping Places")
        print("2. Relaxation Spots")
        print("3. Hiking/Trekking Spots")
        
        while True:
            try:
                choice = int(input("Enter activity type (1-3): "))
                if choice not in activity_types:
                    print("Invalid choice! Try again.")
                    continue
                    
                activity_column = activity_types[choice]
                places_str = df[df["City"] == destination][activity_column].values[0]
                places_list = [place.strip() for place in places_str.split(',')]
                
                print(f"\nAvailable {activity_column} in {destination}:")
                for i, place in enumerate(places_list, 1):
                    print(f"{i}. {place}")
                
                selected = input("\nEnter numbers of places you want to visit (comma separated): ")
                selected_indices = [int(idx.strip()) for idx in selected.split(',') if idx.strip().isdigit()]
                selected_places = [places_list[i-1] for i in selected_indices if 0 < i <= len(places_list)]
                
                if not selected_places:
                    print("No valid selections! Try again.")
                    continue
                
                print(f"\nSelected for Day {day_num}:")
                for place in selected_places:
                    print(f"- {place}")
                
                confirm = input("Confirm? (y/n): ").lower()
                if confirm == 'y':
                    daily_activities[f"Day {day_num}"] = {
                        "activity_type": activity_column,
                        "places": selected_places
                    }
                    break
                    
            except ValueError:
                print("Invalid input! Please enter numbers.")
                continue

    return daily_activities

def transport():
    global n_people, selected_train_details
    s_dest = input("Enter source station name: ").strip().upper()
    e_dest = input("Enter destination station name: ").strip().upper()
    coach_pref = input("Enter preferred coach (Second Class, Sleeper, First Class, AC Chair Car): ").strip().title()

    print("\nFetching train availability...\n")

    try:
        file_path = r"C:\Users\hrushikesh thombare\OneDrive\Desktop\Zip files\train.csv"
        trains_df = pd.read_csv(file_path, dtype=str)

        trains_df.columns = trains_df.columns.str.strip().str.replace(" ", "_")
        trains_df["source_Station_Name"] = trains_df["source_Station_Name"].str.strip().str.upper()
        trains_df["Destination_Station_Name"] = trains_df["Destination_Station_Name"].str.strip().str.upper()
        trains_df["Station_Name"] = trains_df["Station_Name"].str.strip().str.upper()

        source_trains = trains_df[trains_df["Station_Name"] == s_dest]["Train_No."].unique()
        dest_trains = trains_df[trains_df["Station_Name"] == e_dest]["Train_No."].unique()
        common_trains = set(source_trains) & set(dest_trains)

        table_data = []

        for train_no in common_trains:
            train_route = trains_df[trains_df["Train_No."] == train_no]

            try:
                source_row = train_route[train_route["Station_Name"] == s_dest].iloc[0]
                dest_row = train_route[train_route["Station_Name"] == e_dest].iloc[0]

                if source_row.name < dest_row.name:
                    train_name = source_row["train_Name"]
                    departure_time = source_row["Departure_time"]
                    arrival_time = dest_row["Arrival_time"]

                    fare_column = f"{coach_pref.replace(' ', '_')}_Fare"
                    price_per_person = train_route.iloc[0][fare_column] if fare_column in train_route.columns else "N/A"
                    
                    try:
                        total_price = float(price_per_person) * n_people if price_per_person != "N/A" else "N/A"
                    except:
                        total_price = "N/A"

                    table_data.append([
                        str(train_no).strip(),
                        train_name,
                        s_dest,
                        departure_time,
                        e_dest,
                        arrival_time,
                        f"{price_per_person} (Total: {total_price})" if price_per_person != "N/A" else "N/A"
                    ])
            except IndexError:
                continue

        if table_data:
            headers = ["Train No.", "Train Name", "Source", "Departure Time", "Destination", "Arrival Time", "Price (₹)"]
            print("\nAvailable Trains:\n")
            print(tabulate(table_data, headers=headers, tablefmt="grid"))

            selected_train_no = input("\nEnter the Train No. to select a train: ").strip()
            
            selected_train = None
            for train in table_data:
                if train[0] == selected_train_no:
                    selected_train = train
                    break

            if selected_train:
                global t_cost, transport_mode
                selected_train_details = {
                    'number': selected_train[0],
                    'name': selected_train[1],
                    'departure_station': selected_train[2],
                    'departure_time': selected_train[3],
                    'arrival_station': selected_train[4],
                    'arrival_time': selected_train[5],
                    'fare': selected_train[6].split(" (Total: ")[0]
                }
                try:
                    price_str = selected_train[6].split(" (Total: ")[0]
                    t_cost = float(price_str) * n_people if price_str != "N/A" else 0
                except:
                    t_cost = 0
                transport_mode = "Train"
                display(current_location, destination, n_people, s_date, e_date, distance, 
                       transport_mode, t_cost, s, day, c, dish, total_food_cost, 
                       daily_activities, transport_details=selected_train_details)
               
            else:
                print("Invalid train number selected. Please enter exactly as shown.")
        else:
            print("\nNo valid trains found for the selected stations in the correct order.")

    except FileNotFoundError:
        print("Error: CSV file not found.")
    except Exception as e:
        print(f"Error: {e}")

def weather():
    API_KEY = "60d6f3e6a68a434d8e82d6f26374081b" 
    city = input("Enter city: ")
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    data = requests.get(url).json()
    if data.get("main"):
        print(f"\nWeather: {data['weather'][0]['description']}, Temp: {data['main']['temp']}°C, Humidity: {data['main']['humidity']}%")
    else:
        print("City not found!")

def flight():
    global n_people
    s_dest = input("Enter source airport name: ").strip().lower()
    e_dest = input("Enter destination airport name: ").strip().lower()
    print("\nFetching Flight availability...\n")

    try:
        zip_path = r"C:\Users\hrushikesh thombare\OneDrive\Desktop\Zip files\Cleaned_dataset.csv.zip"

        with zipfile.ZipFile(zip_path, 'r') as z:
            csv_filename = z.namelist()[0]
            with z.open(csv_filename) as file:
                flight_df = pd.read_csv(file)

        flight_df.columns = flight_df.columns.str.lower()
        flight_df['source'] = flight_df['source'].astype(str).str.lower().str.strip()
        flight_df['destination'] = flight_df['destination'].astype(str).str.lower().str.strip()

        available_flights = flight_df[
            (flight_df['source'] == s_dest) & 
            (flight_df['destination'] == e_dest)
        ]

        if not available_flights.empty:
            table_data = []
            for _, flight in available_flights.head(5).iterrows():
                try:
                    fare_column = 'fare' if 'fare' in flight else 'price'
                    price_per_person = float(flight[fare_column])
                    total_price = price_per_person * n_people
                    table_data.append([
                        flight['flight_code'],
                        flight['airline'],
                        flight['departure'],
                        flight['arrival'] if 'arrival' in flight else "N/A",
                        f"₹{price_per_person:.2f} (Total: ₹{total_price:.2f})"
                    ])
                except Exception as e:
                    print(f"Error processing flight {flight['flight_code']}: {str(e)}")
                    continue

            headers = ["Flight Code", "Airline", "Departure", "Arrival", "Fare (₹)"]
            print("\nAvailable Flights (Showing 5 results):\n")
            print(tabulate(table_data, headers=headers, tablefmt="grid"))

            selected_flight_code = input("\nEnter the Flight Code to select a flight: ").strip().upper()
            
            selected_flight = None
            for flight in table_data:
                if flight[0].upper() == selected_flight_code:
                    selected_flight = flight
                    break

            if selected_flight:
                global t_cost, transport_mode
                price_str = selected_flight[4].split(" (Total: ₹")[0].replace("₹", "")
                try:
                    t_cost = float(price_str) * n_people
                except:
                    t_cost = 0
                transport_mode = "Flight"
                
                flight_details = {
                    'code': selected_flight[0],
                    'airline': selected_flight[1],
                    'departure_station': s_dest.upper(),
                    'departure_time': selected_flight[2],
                    'arrival_station': e_dest.upper(),
                    'arrival_time': selected_flight[3],
                    'fare': price_str
                }
                
                display(current_location, destination, n_people, s_date, e_date, distance, 
                       transport_mode, t_cost, s, day, c, dish, total_food_cost, 
                       daily_activities, transport_details=flight_details)
            else:
                print("Invalid flight code selected.")
        else:
            print("\nNo flights available for the selected route.")

    except FileNotFoundError:
        print("Error: Flight data file not found.")
    except Exception as e:
        print(f"Error: {str(e)}")

def display(current_location, destination, n_people, s_date, e_date, distance, 
            transport_mode, t_cost, s, day, c, dish, total_food_cost, 
            daily_activities, transport_details=None):
    
    total_cost = c + total_food_cost + t_cost

    # Prepare transport details based on mode
    if transport_mode == "Train" and transport_details:
        transport_info = f"""
🚆 𝗧𝗿𝗮𝗶𝗻 𝗗𝗲𝘁𝗮𝗶𝗹𝘀 🚆
🚂 Train No.: {transport_details['number']}
📛 Name: {transport_details['name']}
📍 From: {transport_details['departure_station']} at {transport_details['departure_time']}
🏁 To: {transport_details['arrival_station']} at {transport_details['arrival_time']}
💰 Fare per person: ₹{transport_details['fare']}
💵 Total Cost: ₹{t_cost:.2f}
"""
    elif transport_mode == "Flight" and transport_details:
        transport_info = f"""
✈️ 𝗙𝗹𝗶𝗴𝗵𝘁 𝗗𝗲𝘁𝗮𝗶𝗹𝘀 ✈️
🛫 Flight: {transport_details['code']}
🏢 Airline: {transport_details['airline']}
📍 From: {transport_details['departure_station']} at {transport_details['departure_time']}
🏁 To: {transport_details['arrival_station']} at {transport_details['arrival_time']}
💰 Fare per person: ₹{transport_details['fare']}
💵 Total Cost: ₹{t_cost:.2f}
"""
    else:
        transport_info = f"""
🚗 𝗧𝗿𝗮𝗻𝘀𝗽𝗼𝗿𝘁 𝗗𝗲𝘁𝗮𝗶𝗹𝘀 🚗
🚗 Mode: {transport_mode}
💰 Cost: ₹{t_cost:.2f}
"""

    # Prepare hotel details with emojis
    hotel_details = f"""
🏨 𝗛𝗼𝘁𝗲𝗹 & 𝗦𝘁𝗮𝘆 𝗗𝗲𝘁𝗮𝗶𝗹𝘀 🏨
⭐ Type: {s}
📅 Duration: {day} days
💵 Cost: ₹{c}
"""

    # Prepare food details with emojis
    food_details = f"""
🍽️ 𝗙𝗼𝗼𝗱 𝗣𝗿𝗲𝗳𝗲𝗿𝗲𝗻𝗰𝗲𝘀 🍽️
🍛 Cuisine: {dish}
💲 Total Cost: ₹{total_food_cost}
"""

    # Prepare activities details with emojis
    activities_details = "\n🎯 𝗗𝗮𝗶𝗹𝘆 𝗔𝗰𝘁𝗶𝘃𝗶𝘁𝗶𝗲𝘀 🎯\n"
    for day_num, activities in daily_activities.items():
        activities_details += f"""
📅 {day_num}:
✨ Type: {activities['activity_type']}
📍 Places: {', '.join(activities['places'])}
"""

    # Create the full itinerary
    itinerary = f"""
✈️・。・。・。・。・。・。・。・。・。・。・✈️
        𝕿𝖗𝖆𝖛𝖊𝖑 𝕴𝖙𝖎𝖓𝖊𝖗𝖆𝖗𝖞 𝕻𝖑𝖆𝖓𝖓𝖊𝖗
✈️・。・。・。・。・。・。・。・。・。・。・✈️

🌍 𝗧𝗿𝗶𝗽 𝗗𝗲𝘁𝗮𝗶𝗹𝘀 🌍
📍 From: {current_location}
🏁 To: {destination}
👥 People: {n_people}
📅 Dates: {s_date} to {e_date}
📏 Distance: {distance:.2f} km

{transport_info}
{hotel_details}
{food_details}
{activities_details}

💰 𝗖𝗼𝘀𝘁 𝗕𝗿𝗲𝗮𝗸𝗱𝗼𝘄𝗻 💰
🚗 Transport: ₹{t_cost:.2f}
🏨 Hotel: ₹{c}
🍽️ Food: ₹{total_food_cost}
💵 𝗧𝗼𝘁𝗮𝗹 𝗰𝗼𝘀𝘁: ₹{total_cost:.2f}

✨・。・。・。・。・。・。・。・。・。・。・✨
       𝓗𝓪𝓿𝓮 𝓪 𝓰𝓻𝓮�𝓽 𝓽𝓻𝓲𝓹! 
✨・。・。・。・。・。・。・。・。・。・。・✨
"""

    print(itinerary)

# Main program
print("-----Welcome to Travel Itinerary Planner-----\n")
n = 1
while n != 0:
    choice = int(input("1. Create New Itinerary\n2. Hotel Details\n3. Weather Details \n4. Tourist Places\n5. Transport Details\nEnter your choice (1-5) : "))
    if choice == 1:
        current_location, destination = insertdetails()
        coords1 = get_coordinates(current_location)
        coords2 = get_coordinates(destination)

        if coords1 and coords2:
            lat1, lon1 = coords1
            lat2, lon2 = coords2

        distance = haversine(lat1, lon1, lat2, lon2)
        s_date = input("Enter start date (YYYY-MM-DD) : ")
        e_date = input("Enter end date (YYYY-MM-DD) : ")
    elif choice == 2:
        c, s, day, total_food_cost = hotel()
    elif choice == 3:
        weather()
    elif choice == 4: 
        daily_activities = activities(destination, day)
    elif choice == 5:
        print("\nChoose your mode of transport:")
        print("1. Car (₹15 per km)")
        print("2. Bus (₹1.675 per km)")
        print("3. Train")
        print("4. Flight")
        transport_choice = int(input("Enter your choice (1-4) : "))
        
        if transport_choice == 1:
            transport_mode = "Car"
            t_cost = distance * 15 * n_people
            print(f"\nCar transport cost for {distance:.2f} km for {n_people} people: ₹{t_cost:.2f}")
            display(current_location, destination, n_people, s_date, e_date, distance, 
                   transport_mode, t_cost, s, day, c, dish, total_food_cost, daily_activities)
            
        elif transport_choice == 2:
            transport_mode = "Bus"
            t_cost = distance * 1.675 * n_people
            print(f"\nBus transport cost for {distance:.2f} km for {n_people} people: ₹{t_cost:.2f}")
            display(current_location, destination, n_people, s_date, e_date, distance, 
                   transport_mode, t_cost, s, day, c, dish, total_food_cost, daily_activities)
            
        elif transport_choice == 3:
            transport()
            
        elif transport_choice == 4:
            flight()
            
        else:
            print("Invalid choice!")
    else:
        print("Invalid choice")
    n = int(input("\nDo you want to continue(1/0) ? : "))
