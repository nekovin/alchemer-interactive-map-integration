const parkData = [
  {
    name: "Carlton Gardens",
    //color: "#4CAF50", // Unselected translucent green
    defaultColor: "#2E7D32",
    selectedColor: "#FF9800",
    coords: [
      { lat: -37.800931, lng: 144.970184 },
      { lat: -37.801642, lng: 144.973030 },
      { lat: -37.807802, lng: 144.970921 },
      { lat: -37.807096, lng: 144.968078 }
    ]
  },
  {
    name: "Fitzroy Gardens",
    //color: "#2E7D32", // Darker unselected green
    defaultColor: "#2E7D32",
    selectedColor: "#FF9800",
    coords: [
      { lat: -37.809565, lng: 144.976071 },
      { lat: -37.810565, lng: 144.982937 },
      { lat: -37.816439, lng: 144.981843 },
      { lat: -37.815371, lng: 144.974955 }
    ]
  }
];

const ALCHEMER_HIDDEN_FIELD_ID = "sgE-391014007-2-19-element" // mTHIS NEEDS TO BE MAINTAINED IF SOMEBODY SCREWS W MY CODE >:(

let userSelections = [];

window.initAlchemerMap = function() {
  const mapElement = document.getElementById("map");
  if (!mapElement) return;

  const map = new google.maps.Map(mapElement, {
    zoom: 15,
    center: { lat: -37.8080, lng: 144.9750 },
    mapTypeId: "roadmap"
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
