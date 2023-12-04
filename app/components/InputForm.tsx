"use client";

import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import * as z from "zod";

import { Button } from "../components/ui/button";
import Autocomplete from "react-google-autocomplete";

import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "../components/ui/form";
import { Input } from "../components/ui/input";
import { toast } from "../components/ui/use-toast";
import axios from "axios";
import { useState } from "react";

type ApiResponse = {
  source_address: string;
  destination_address: string;
};

// import Cors from 'cors';
// import { runMiddleware } from '../../utils/runMiddleware';

// // Initializing the cors middleware
// const cors = Cors({
//   methods: ['GET'],
// });



const FormSchema = z.object({
  source_address: z.string().min(2, {
    message: "Starting point must be at least 2 characters.",
  }),
  destination_address: z.string().min(2, {
    message: "Destination must be at least 2 characters.",
  }),
});

export function InputForm({setIsCome}: any) {
  const form = useForm<z.infer<typeof FormSchema>>({
    resolver: zodResolver(FormSchema),
    defaultValues: {
      source_address: "",
      destination_address: "",
    },
  });

  const [dataResponse, setDataResponse] = useState<ApiResponse | null>();
  

  function onSubmit(data: z.infer<typeof FormSchema>) {
    setIsCome(true);
    
    console.log(data);
    fetchResponce(data);
    return null
  }

  const fetchResponce = async (data: any) => {
    try {
      // const response = await axios.get(`/get_routes_coordinates?source_address=${data.source_address}&destination_address=${data.destination_address}`
      // );

      console.log(data)
      const response = await axios.get(`http://127.0.0.1:3000/get_routes_coordinates?source_address=washington-square-park&destination_address=bobst-library`
      );
      // setDataResponse(response.data);
      // console.log(response.data);

      return response;
    } catch (error) {
      console.error("Failed to fetch disciplines:", error);
    }
  };

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="w-full space-y-6">
        <FormField
          control={form.control}
          name="source_address"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Starting Point</FormLabel>
              <FormControl>
                <Input placeholder="Enter starting point" {...field} />
              </FormControl>
              {/* <FormDescription>This could be address</FormDescription> */}
              <FormMessage />
            </FormItem>
          )}
        />
        {/* <Autocomplete
          apiKey={process.env.NEXT_PUBLIC_GOOGLE_MAPS_API_KEY as string}
          onPlaceSelected={(place) => {
            console.log(place);
          }}
          >
             */}

        <FormField
          control={form.control}
          name="destination_address"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Destination</FormLabel>
              <FormControl>
                <Input placeholder="Enter destination" {...field} />
              </FormControl>
              {/* <FormDescription>This could be address</FormDescription> */}
              <FormMessage />
            </FormItem>
          )}
        />
        <Button type="submit">Find routes</Button>
      </form>
    </Form>
  );
}
