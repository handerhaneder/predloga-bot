import { webhookCallback } from "https://esm.sh/grammy@1.34.0";
import { bot } from "./bot.ts";

const handleUpdate = webhookCallback(bot, "std/http");

Deno.serve(async (req) => {
  try {
    return await handleUpdate(req);
  } catch (e) {
    console.error(e);
    return new Response("Error", { status: 500 });
  }
});
