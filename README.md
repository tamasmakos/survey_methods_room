# Find Closest Place
This script provides a function getClosestPlace() that uses the Google Maps Places API to find the closest place of a specified type to a given location.

## Function
function getClosestPlace(latitude, longitude, radius, placeType)
This function takes the following parameters:

latitude and longitude: The coordinates of the location.
radius: The search radius in meters.
placeType: The type of place to search for, such as restaurant, hospital, etc.
It returns a 2D array with the name and distance (in meters) of the closest place.

## Usage
Here is an example of how to use this function:

var result = getClosestPlace(47.497913, 19.040236, 5000, "restaurant");
console.log(result[0][0] + " is " + result[0][1] + " meters away.");

## Prerequisites
You need to have a Google Maps API key to use this function. Replace "API" with your Google Maps API key in the apiKey variable.

## Validation
The function validates the latitude, longitude, and radius parameters. If they are not valid, it throws an error.

## Error Handling
If an error occurs when searching for nearby places, the function throws an error with the status returned by the Google Maps Places API.

## Distance Calculation
The function uses the haversine formula to calculate the great-circle distance between two points on the Earth's surface, which is the shortest distance over the Earth's surface.

### Note
This script is written in JavaScript for use with Google Apps Script. It can be used in a Google Sheets script editor or any other environment where Google Apps Script runs.

### Usage in Google Sheets

#### GET GEOCODES
The function takes the address as parameter and returns the Latitude and Longitude
<img width="776" alt="Screenshot 2023-05-11 at 14 13 55" src="https://github.com/tamasmakos/find_nearby_places/assets/86356871/35d7f7e1-b805-4e0d-ba59-260fc355454a">


#### GET CLOSES POINT OF INTEREST
The function have three argument:
- Latitude
- Longitude
- Radius
- Type of place

Returns the name and the distance of the closest type of place

<img width="776" alt="Screenshot 2023-05-11 at 14 14 42" src="https://github.com/tamasmakos/find_nearby_places/assets/86356871/a33d03c5-7e72-42e1-9bee-254191537040">
