import { Bot } from "https://esm.sh/grammy@1.34.0";
import { addRequest, getAllRequests } from "./db.ts";

const BOT_TOKEN = Deno.env.get("BOT_TOKEN")!;
const CREATOR_ID = parseInt(Deno.env.get("CREATOR_ID")!);

export const bot = new Bot(BOT_TOKEN);

function mainKeyboard(userId: number) {
  const keyboard = [["📨 Послать запрос на совместный блог"]];
  if (userId === CREATOR_ID) keyboard.push(["📋 Посмотреть запросы"]);
  return { keyboard, resize_keyboard: true };
}

function formatDate(iso: string): string {
  const d = new Date(iso);
  const pad = (n: number) => n.toString().padStart(2, "0");
  return `${pad(d.getDate())}.${pad(d.getMonth() + 1)}.${d.getFullYear()} ${pad(d.getHours())}:${pad(d.getMinutes())}`;
}

bot.command("start", async (ctx) => {
  await ctx.reply(
    "👋 Добро пожаловать в <b>писмо хандеру</b>!\n\nХочешь вести совместный блог? Отправь запрос — и я передам его создателю.\n\nВыбери действие ниже",
    { parse_mode: "HTML", reply_markup: mainKeyboard(ctx.from!.id) }
  );
});

bot.hears("📨 Послать запрос на совместный блог", async (ctx) => {
  const user = ctx.from!;
  const username = user.username ? `@${user.username}` : "нет username";
  const fullName = [user.first_name, user.last_name].filter(Boolean).join(" ") || "нет имени";

  await addRequest(user.id, fullName, username);

  try {
    await ctx.api.sendMessage(
      CREATOR_ID,
      `🔔 <b>Новый запрос на совместный блог!</b>\n\n👤 Имя: ${fullName}\n🔗 Username: ${username}\n🆔 ID: <code>${user.id}</code>\n\n<a href='tg://user?id=${user.id}'>📩 Написать напрямую</a>`,
      { parse_mode: "HTML" }
    );
  } catch (e) {
    console.warn("Не удалось уведомить создателя:", e);
  }

  await ctx.reply(
    "✅ <b>Запрос отправлен!</b>\n\nСоздатель блога получил твои контактные данные и скоро свяжется с тобой. 🎉",
    { parse_mode: "HTML" }
  );
});

bot.hears("📋 Посмотреть запросы", async (ctx) => {
  if (ctx.from!.id !== CREATOR_ID) {
    await ctx.reply("⛔ У тебя нет доступа к этой функции.");
    return;
  }

  const requests = await getAllRequests();

  if (!requests.length) {
    await ctx.reply("📭 Запросов пока нет.");
    return;
  }

  let text = `📋 <b>Все запросы (${requests.length}):</b>\n\n`;
  for (const [i, req] of requests.entries()) {
    text += `${i + 1}. 👤 <b>${req.full_name}</b>\n   🔗 ${req.username}\n   🆔 <code>${req.user_id}</code>\n   <a href='tg://user?id=${req.user_id}'>📩 Написать</a>\n   📅 ${formatDate(req.created_at)}\n\n`;
  }

  for (let i = 0; i < text.length; i += 4000) {
    await ctx.reply(text.slice(i, i + 4000), { parse_mode: "HTML", disable_web_page_preview: true });
  }
});
