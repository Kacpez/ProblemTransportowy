import React from "react";
import { useState,useEffect } from "react";
import { MapContainer, TileLayer,Polyline ,Marker,Popup} from "react-leaflet";
import {Icon} from "leaflet";

var greenIcon = new Icon({
  iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-orange.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41]
});

const blueOptions = { fillColor: 'blue' ,weight:5 ,opacity:0.7}
const tealOptions = { color: 'teal', weight: 5, opacity: 0.7 };
const yellowOptions = { color: 'yellow', weight: 5, opacity: 0.7 };
const greenOptions = { color: 'darkgreen',weight:5 ,opacity:0.7}
const purpleOptions = { color: 'purple',weight:5 ,opacity:0.7 }
const redOptions = { color: 'red' ,weight:5 ,opacity:0.7}
const blackOptions = { color: 'black',weight:5,opacity:0.7 }
const orangeOptions = { color: 'orange', weight: 5, opacity: 0.7 };
const pinkOptions = { color: 'pink', weight: 5, opacity: 0.7 };
const brownOptions = { color: 'brown', weight: 5, opacity: 0.7 };
const cyanOptions = { color: 'cyan', weight: 5, opacity: 0.7 };
const magentaOptions = { color: 'magenta', weight: 5, opacity: 0.7 };
const limeOptions = { color: 'lime', weight: 5, opacity: 0.7 };
const indigoOptions = { color: 'indigo', weight: 5, opacity: 0.7 };
const violetOptions = { color: 'violet', weight: 5, opacity: 0.7 };

const colors = [
  blueOptions,
  greenOptions,
  redOptions,
  orangeOptions,
  purpleOptions,
  tealOptions,
  blackOptions,
  pinkOptions,
  brownOptions,
  cyanOptions,
  magentaOptions,
  limeOptions,
  indigoOptions,
  violetOptions,
  
  blueOptions,
  greenOptions,
  redOptions,
  orangeOptions,
  purpleOptions,
  tealOptions,
  blackOptions,
  pinkOptions,
  brownOptions,
  cyanOptions,
  magentaOptions,
  limeOptions,
  indigoOptions,
  violetOptions,
  yellowOptions,
  yellowOptions
];

const Map = (props) => {

  const [dane, setDane] = useState({ bakeries: [], cafes: [] });
  const [selectedSegments, setSelectedSegments] = useState([]);
  const [showAllSegments, setShowAllSegments] = useState(true);
  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch("http://127.0.0.1:5000/cele", {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
          },
        });

        if (!response.ok) {
          throw new Error("Błąd pobierania danych");
        }

        const data = await response.json();
        setDane(data);

      } catch (error) {
        console.error("Błąd:", error);
      }
    };

    fetchData();
  }, []); 

  const handleSegmentCheckboxChange = (index) => {
    const updatedSelectedSegments = [...selectedSegments];
    updatedSelectedSegments[index] = !updatedSelectedSegments[index];
    setSelectedSegments(updatedSelectedSegments);
  };

  const handleShowAllCheckboxChange = () => {
    setShowAllSegments(!showAllSegments);
  };
 
  return (
    <>
 <div className="container">
        {props.trasy.map((trasa, index) => (
          <div key={index} >
           
            <input class="btn-check" id={`btn-check-outlined-${props.liczba}-${index+1}`} autocomplete="off" 
              type="checkbox"
              checked={selectedSegments[index] || showAllSegments}
              onChange={() => handleSegmentCheckboxChange(index)}
            />
            <label  class="btn btn-outline-primary" htmlFor={`btn-check-outlined-${props.liczba}-${index+1}`}>Pokaż trasę {index + 1}</label>
          </div>
        ))}
        
        {props.liczba>0 && <> <input class="btn-check" id={`btn-check-outlined-${props.liczba}-${0}`} autocomplete="off" disabled={props.liczba === 0}
          type="checkbox"
          checked={showAllSegments}
          onChange={handleShowAllCheckboxChange}
        />
        <label class="btn btn-outline-secondary" htmlFor={`btn-check-outlined-${props.liczba}-${0}`}>Pokaż wszytkie trasy</label>
        </>}
        </div>
      <MapContainer  center={props.centerList} zoom={13} scrollWheelZoom={false}>
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        {dane.bakeries.map((coordinates, index) => (
          <Marker key={index} position={[coordinates[1], coordinates[0]]} pathOptions={redOptions} >
            <Popup>
        Piekarnia {index+1}
      </Popup>
      </Marker>
        ))}
        {dane.cafes.map((coordinates, index) => (
          <Marker key={index} position={[coordinates[1], coordinates[0]]} icon={greenIcon} pathOptions={redOptions} >
          <Popup>
      Kawiarnia {index+1}
    </Popup>
    </Marker>
        ))}
        {props.trasy.map((trasa, index) => (
           <React.Fragment key={index}>
           {showAllSegments || selectedSegments[index] ? (
             <React.Fragment>
               {trasa.map((segment, segmentIndex) => (
                 <Polyline
                   key={segmentIndex}
                   pathOptions={colors[index]}
                   positions={segment}
                 />
               ))}
             </React.Fragment>
           ) : null}
         </React.Fragment>
        ))}
      </MapContainer>
      <br></br>
      </>
  )
};

export default Map;