import React, { useEffect, useRef, useState, useMemo } from 'react';
import L from 'leaflet';
import axios from "axios";


const LeafletMap = () => {

  //lat and longitude
  const [addressTextField, setAddressTextField] = useState("");
  const [address, setAddress] = useState([51.505, -0.09]);

  const mapRef = useRef(null); // Reference for the map container
  const mapInstance = useRef(null); // To store the Leaflet map instance
  const [markers, setMarkers] = useState([]); // State to track markers
  const [selectedColor, setSelectedColor] = useState('blue'); // State for marker color


  const handleAddressChange = async () => {
    console.log(addressTextField)


    const formData = new FormData();
    //formData.append(address);
    //formData.append("text", "24215 Abbeywood Dr");

    formData.append("text", addressTextField);


    try {
      const response = await axios.post(
        "http://127.0.0.1:5000/upload_address",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );
      console.log("Upload successful:", response.data);
      console.log(response.data[0]["lat"], " | ", response.data[0]["lon"])

      mapInstance.current.setView([response.data[0]["lat"], response.data[0]["lon"]], 13);

      setAddress([response.data[0]["lat"], response.data[0]["lon"]])


      //handleUploadSuccess(response.data);
    } catch (error) {
      console.error("Error uploading file:", error);
    }

  };



  // Marker icons by color, memoized to prevent recreation on each render
  const markerIcons = useMemo(() => ({
    blue: L.icon({
      iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
      iconSize: [25, 41],
      iconAnchor: [12, 41],
    }),
    red: L.icon({
      iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-red.png',
      iconSize: [25, 41],
      iconAnchor: [12, 41],
    }),
    green: L.icon({
      iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-green.png',
      iconSize: [25, 41],
      iconAnchor: [12, 41],
    }),
  }), []);

  // Initialize the map only once
  useEffect(() => {
    if (!mapRef.current) return;

    // Initialize the map
    //mapInstance.current = L.map(mapRef.current).setView([51.505, -0.09], 13);
    mapInstance.current = L.map(mapRef.current).setView(address, 13);

    // Add OpenStreetMap tile layer
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    }).addTo(mapInstance.current);

    // Click event to add markers
    mapInstance.current.on('click', (event) => {
      const { lat, lng } = event.latlng;
      const marker = L.marker([lat, lng], { icon: markerIcons[selectedColor] }).addTo(mapInstance.current);
      setMarkers((prevMarkers) => [...prevMarkers, marker]);

      // Add click event to marker for removal
      marker.on('click', () => {
        mapInstance.current.removeLayer(marker); // Remove marker from map
        setMarkers((prevMarkers) => prevMarkers.filter((m) => m !== marker)); // Remove marker from state
      });
    });

    // Cleanup on component unmount
    return () => {
      mapInstance.current.remove();
    };
  }, [markerIcons, selectedColor]); // Note: selectedColor is removed from dependencies

  // Update marker icons when selectedColor changes
  useEffect(() => {
    markers.forEach((marker) => {
      marker.setIcon(markerIcons[selectedColor]);
    });
  }, [selectedColor, markerIcons, markers]);


  const handleInputChange = (event) => {
    setAddressTextField(event.target.value);
  };


  return (
    <div>

    <input
          type="text"
          placeholder="Enter address"
          style={{ marginRight: '10px', padding: '5px' }}
          onChange={handleInputChange}
    />

    <button onClick={handleAddressChange}>SUBMIT</button>


      <div ref={mapRef} style={{ height: '500px', width: '100%' }} />

      {/* Color Options */}
      <div style={{ marginTop: '10px', display: 'flex', alignItems: 'center', gap: '10px' }}>
        <span>Select Marker Color:</span>
        <button
          style={{
            backgroundColor: 'blue',
            color: 'white',
            padding: '5px 10px',
            border: 'none',
            borderRadius: '5px',
          }}
          onClick={() => setSelectedColor('blue')}
        >
          Blue
        </button>
        <button
          style={{
            backgroundColor: 'red',
            color: 'white',
            padding: '5px 10px',
            border: 'none',
            borderRadius: '5px',
          }}
          onClick={() => setSelectedColor('red')}
        >
          Red
        </button>
        <button
          style={{
            backgroundColor: 'green',
            color: 'white',
            padding: '5px 10px',
            border: 'none',
            borderRadius: '5px',
          }}
          onClick={() => setSelectedColor('green')}
        >
          Green
        </button>
        <button
          style={{
            marginLeft: 'auto',
            backgroundColor: 'gray',
            color: 'white',
            padding: '5px 10px',
            border: 'none',
            borderRadius: '5px',
          }}
          onClick={() => {
            markers.forEach((marker) => marker.remove()); // Remove all markers
            setMarkers([]); // Clear marker state
          }}
        >
          Clear All Pins
        </button>
      </div>

      {/* Legend */}
      <div
        style={{
          marginTop: '20px',
          border: '1px solid #ccc',
          padding: '10px',
          borderRadius: '5px',
          width: '300px',
        }}
      >
        <h4>Legend</h4>
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <div
            style={{
              backgroundColor: 'blue',
              width: '20px',
              height: '20px',
              borderRadius: '50%',
            }}
          ></div>
          <span>Blue: Default</span>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <div
            style={{
              backgroundColor: 'red',
              width: '20px',
              height: '20px',
              borderRadius: '50%',
            }}
          ></div>
          <span>Red: Important</span>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <div
            style={{
              backgroundColor: 'green',
              width: '20px',
              height: '20px',
              borderRadius: '50%',
            }}
          ></div>
          <span>Green: Completed</span>
        </div>
      </div>
    </div>
  );
};

export default LeafletMap;
