import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

const supabase = createClient(
  Deno.env.get("SUPABASE_URL")!,
  Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!
);

export async function addRequest(userId: number, fullName: string, username: string) {
  const { error } = await supabase.from("requests").insert({ user_id: userId, full_name: fullName, username });
  if (error) throw error;
}

export async function getAllRequests() {
  const { data, error } = await supabase
    .from("requests")
    .select("user_id, full_name, username, created_at")
    .order("created_at", { ascending: false });
  if (error) throw error;
  return data ?? [];
}
