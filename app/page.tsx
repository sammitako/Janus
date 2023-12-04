"use client";
/*global google*/

import Image from "next/image";
import { Inter } from "next/font/google";
import { Button } from "./components/ui/button";
import { InputForm } from "./components/InputForm";
// import { GoogleMap, useLoadScript } from "@react-google-maps/api";
import GoogleMapReact from "google-map-react";
import { useState } from "react";
const AnyReactComponent = ({ text }: any) => <div>{text}</div>;

const inter = Inter({ subsets: ["latin"] });
const center = { lat: 40.728899561324454, lng: -73.99569061868435 };
export default function Home() {
  // const { isLoaded } = useLoadScript({
  //   googleMapsApiKey: process.env.NEXT_PUBLIC_GOOGLE_MAPS_API_KEY as string,
  // });
  const handleApiLoaded = (map: any, maps: any) => {
    const directionsService = new google.maps.DirectionsService();
    const directionsRenderer = new google.maps.DirectionsRenderer();
    directionsRenderer.setMap(map);
    const origin = { lat: 40.756795, lng: -73.954298 };
    const destination = { lat: 41.756795, lng: -78.954298 };

    directionsService.route(
      {
        origin: origin,
        destination: destination,
        travelMode: google.maps.TravelMode.DRIVING,
      },
      (result, status) => {
        if (status === google.maps.DirectionsStatus.OK) {
          directionsRenderer.setDirections(result);
        } else {
          console.error(`error fetching directions ${result}`);
        }
      }
    );
  };

  const [isCome, setIsCome] = useState(false);



  return (
    <main className="h-full w-full ">
      <div className="grid grid-cols-8 max-w-5xl mx-auto">
        {/* TITLE */}
        <div className="col-span-3 mx-auto text-6xl place-self-center">
          <p>Find Safest Routes.</p>
          <p>Be Safe.</p>
        </div>
        {/* INPUT */}
        <div className="col-span-5 ml-10">
          <InputForm setIsCome={setIsCome} />
        </div>
      </div>
      <div className="border w-full max-w-5xl mx-auto mt-8 p-2 rounded-lg">
        {isCome && (
          <>
          
          <p className="font-bold text-lg ">Safest Route to Take</p>
          <p>Route 1: [40.731373, -73.997014], [40.7314265, -73.9968434], [40.7644559, -73.9730483]</p>
          <p>Distance: 2.6 mi</p>
          <p>Risk Score: 23</p>
          <p>Time: 59 mins</p>
          <br></br>
          <p>Route 2: [40.7307395, -73.9956729], [40.73071909999999, -73.99569269999999], [40.7306453, -73.9955351], [40.7350833, -73.99167539999999], [40.73722009999999, -73.9903777], [40.74287169999999, -73.9885659], [40.7644559, -73.9730483]</p>
          <p>Distance: 2.6 mi</p>
          <p>Risk Score: 145</p>
          <p>Time: 1 hour 0 mins</p>
          <br></br>
          <p>Route 3: [40.73214, -73.9985975], [40.732265, -73.998544], [40.7329396, -73.9999146], [40.7657686, -73.9761048], [40.7659646, -73.97658179999999]</p>
          <p>Distance: 2.7 mi</p>
          <p>Risk Score: 48</p>
          <p>Time: 1 hour 2 mins</p>
          </>
        )}
      
      </div>

      {/* MAP */}
      {/* global google */}
      {/* <GoogleMap
        center={center}
        zoom={15}
        mapContainerStyle={{ width: "100%", height: "100%" }}
      ></GoogleMap> */}
      <div className="h-screen w-full mt-10 ">
        <GoogleMapReact
          bootstrapURLKeys={{
            key: process.env.NEXT_PUBLIC_GOOGLE_MAPS_API_KEY as string,
          }}
          defaultCenter={center}
          defaultZoom={15}
          yesIWantToUseGoogleMapApiInternals
          onGoogleApiLoaded={({ map, maps }) => handleApiLoaded(map, maps)}
        >
          <AnyReactComponent lat={59.955413} lng={30.337844} text="My Marker" />
        </GoogleMapReact>
      </div>
    </main>
  );
}
