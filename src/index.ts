// src/Index.ts 
// run the server here

import { connectDB } from "./db";
import { createAuth } from "./shared/services/auth";
import { createApp } from "./app";

const server = async () => {
  const mongoClient = await connectDB();
  createAuth(mongoClient);

  const app = createApp();
  app
    .onRequest(({ request }) => {
      // `request.method` and `request.url` are standard Web API values
      console.log(`[${new Date().toISOString()}] ${request.method} ${new URL(request.url).pathname}`)
      // you can also log query, headers, etc.
    })
    .listen(3000, ({ hostname, port }) => {
      console.log(`Elysia running on http://${hostname}:${port}`)
    })
};

server();



