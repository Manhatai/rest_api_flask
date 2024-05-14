import requests

BASE = "http://127.0.0.1:5000/"


#print("ClientsList get response:")
#response = requests.get(BASE + "/clients") # a get request
#print(response.json()) # Successfully returns data in json format

#print("\nClients get reponse:")
#response = requests.get(BASE + "/clients/andrzej") 
#print(response.json()) 

#print("\nCarsList get response:")
#response = requests.get(BASE + "/cars") 
#print(response.json()) 

#print("\nCars get reponse:")
#response = requests.get(BASE + "/cars/bmw1") 
#print(response.json()) 

#print("\nBookingList get response:")
#response = requests.get(BASE + "/booking") 
#print(response.json())

#print("\nBooking get reponse:")
#response = requests.get(BASE + "/booking/00023")
#print(response.json()) 

print("\nBooking get reponse:")
response = requests.put(BASE + "booking/12345", {"date": "11:06.2024"})
print(response.json())