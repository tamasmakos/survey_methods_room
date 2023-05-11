function getClosestPlace(latitude, longitude, radius, placeType) {
    var apiKey = "API"; // Replace with your Google Maps API key
  
    // Validate latitude, longitude, and radius
    if (latitude < -90 || latitude > 90 || longitude < -180 || longitude > 180 || radius <= 0) {
      throw new Error("Invalid latitude, longitude, or radius");
    }
  
    // Search for nearby places
    var placesUrl = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=" + latitude + "," + longitude + "&radius=" + radius + "&type=" + placeType + "&key=" + apiKey;
    var placesResponse = UrlFetchApp.fetch(placesUrl);
    var placesData = JSON.parse(placesResponse.getContentText());
  
    if (placesData.status !== "OK") {
      throw new Error("Error finding nearby places: " + placesData.status);
    }
  
    if (placesData.results.length === 0) {
      return [["Nincs találat", ""]];
    }
  
    // Find the closest place and its distance
    var closestPlace = placesData.results[0];
    var closestDistance = getDistance(latitude, longitude, closestPlace.geometry.location.lat, closestPlace.geometry.location.lng);
  
    for (var i = 1; i < placesData.results.length; i++) {
      var place = placesData.results[i];
      var distance = getDistance(latitude, longitude, place.geometry.location.lat, place.geometry.location.lng);
  
      if (distance < closestDistance) {
        closestPlace = place;
        closestDistance = distance;
      }
    }
  
    return [[closestPlace.name, closestDistance.toFixed(0)]];
  }
  
  function getDistance(lat1, lon1, lat2, lon2) {
    var R = 6371000; // Radius of the Earth in meters
    var dLat = toRad(lat2 - lat1);
    var dLon = toRad(lon2 - lon1);
    var a = Math.sin(dLat / 2) * Math.sin(dLat / 2) + Math.cos(toRad(lat1)) * Math.cos(toRad(lat2)) * Math.sin(dLon / 2) * Math.sin(dLon / 2);
    var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    return R * c;
  }
  
  function toRad(value) {
    return value * Math.PI / 180;
  }
  