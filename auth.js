import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

const SUPABASE_URL = "https://qzgxowcywdhkhvphbpsq.supabase.co";
const SUPABASE_KEY = "sb_publishable_M-8MzpQ8zY5AMhMy82uxpw_g11UesBo";

export const supabase = createClient(SUPABASE_URL, SUPABASE_KEY);

export async function signUp(email, password) {
    return await supabase.auth.signUp({
        email,
        password,
        options: {
            emailRedirectTo: window.location.origin + "/dashboard.html",
        },
    });
}

export async function signIn(email, password) {
    return await supabase.auth.signInWithPassword({
        email,
        password,
    });
}

export async function signInWithGoogle() {
    return await supabase.auth.signInWithOAuth({
        provider: "google",
        options: {
            redirectTo: window.location.origin + "/dashboard.html",
        },
    });
}

export async function logout() {
    await supabase.auth.signOut();
    window.location.href = "/index.html";
}

export async function protectPage() {
    const { data: { session } } = await supabase.auth.getSession();

    if (!session) {
        window.location.href = "/index.html";
    }
}