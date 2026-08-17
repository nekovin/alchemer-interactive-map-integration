const finalAzureUrl = 'https://alchemer01.blob.core.windows.net/4463/parks_data/parks_data.json?sp=r&st=2026-07-01T05:48:03Z&se=2026-07-29T14:03:03Z&spr=https&sv=2026-02-06&sr=b&sig=qw578tyhKN%2FJLu60G2eBMA7nDDrVpjGrgtuHKP%2FJogo%3D'

fetch(finalAzureUrl, {
  method: "GET",
  mode: "cors"
})
  .then(response => {
    if (!response.ok) throw new Error(`Azure HTTP Error: ${response.status}`);
    return response.json();
  })
  .then(jsonData => {
    // Save the data to your global variable instead of putting logic here
    window.azureParksData = jsonData;
    
    console.log("data saved");
    
    console.log(jsonData);
  })
  .catch(error => {
    console.error("Fetch failed:", error);
  });


const ALCHEMER_HIDDEN_FIELD_ID = "sgE-391014007-2-19-element" // mTHIS NEEDS TO BE MAINTAINED IF SOMEBODY SCREWS W MY CODE >:(

let userSelections = [];

window.initAlchemerMap = function() {
  if (!window.azureParksData) {
    console.log("Park data not ready yet, retrying...");
    setTimeout(window.initAlchemerMap, 100);
    return;
  }

  const parkData = window.azureParksData;
  console.log("Park Data:", parkData);

  const mapElement = document.getElementById("map");
  if (!mapElement) return;

  const map = new google.maps.Map(mapElement, {
    zoom: 15,
    center: { lat: -37.8080, lng: 144.9750 },
    mapTypeId: "roadmap"
  });

  map.addListener('tilesloaded', () => {
    const loader = document.getElementById('map-loader');
    if (loader) loader.style.display = 'none';
  });
  
  parkData.forEach(park => {
            let isSelected = false; //track selection

            const polygonHighlight = new google.maps.Polygon({
              paths: park.coords,
              strokeColor: park.defaultColor,
              strokeOpacity: 0.8,
              strokeWeight: 2,
              fillColor: park.defaultColor,
              fillOpacity: 0.35,
              map: map
            });
  
google.maps.event.addListener(polygonHighlight, 'click', function() {
  isSelected = !isSelected; // Toggle the state

  if (isSelected) {
    polygonHighlight.setOptions({
      fillColor: park.selectedColor,
      strokeColor: park.selectedColor
    });
    
    if (!userSelections.includes(park.name)) {
      userSelections.push(park.name);
    }
  } else {
    polygonHighlight.setOptions({
      fillColor: park.defaultColor,
      strokeColor: park.defaultColor
    });
    
    userSelections = userSelections.filter(item => item !== park.name);
  }

  console.log("Current Selections Array:", userSelections);

  const alchemerField = document.getElementById(ALCHEMER_HIDDEN_FIELD_ID);//"sgE-391014007-2-19-element");
  if (alchemerField) {
  
    alchemerField.value = userSelections.join(", ");
    
    // 2. tell Alchemer's background system that the text box has changed
    const changeEvent = new Event('change', { bubbles: true });
    alchemerField.dispatchEvent(changeEvent);
  }
  // ===============================================
});

  
});
  
};



(function() {
  if (window.google && window.google.maps) {
    
    window.initAlchemerMap();
  } else {
    const script = document.createElement("script");
    

    script.src = "https://maps.googleapis.com/maps/api/js?key=AIzaSyBnhF8F278dHno51nyrbqBEQn_rELO4mQE&callback=initAlchemerMap";
    script.type = "text/javascript";
    script.async = true;
    script.defer = true;
    
    document.head.appendChild(script);
  }
})();
