function geocodeAddress(address) {
    var apiKey = "API"; // Replace with your Google Maps API key
    
    // Geocode the address
    var geocodeUrl = "https://maps.googleapis.com/maps/api/geocode/json?address=" + encodeURIComponent(address) + "&key=" + apiKey;
    var geocodeResponse = UrlFetchApp.fetch(geocodeUrl);
    var geocodeData = JSON.parse(geocodeResponse.getContentText());
    
    if (geocodeData.status === "OK") {
      var latitude = geocodeData.results[0].geometry.location.lat;
      var longitude = geocodeData.results[0].geometry.location.lng;
      
      return {
        address: address,
        coordinates: latitude + ", " + longitude
      };
    } else {
      throw new Error("Error geocoding address: " + geocodeData.status);
    }
  }
  
  function getAddressCoordinates(address) {
    try {
      var data = geocodeAddress(address);
      return [
        [data.coordinates]
      ];
    } catch (error) {
      return error.message;
    }
  }
  