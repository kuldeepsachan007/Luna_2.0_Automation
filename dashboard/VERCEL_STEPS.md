# Vercel par dashboard daalne ke poore steps (Hinglish)

## 0. Mental model (pehle samajh lo)
- **Vercel par sirf UI jaati hai** (`index.html`). Ye ek web page host karta hai — permanent URL deta hai.
- **Tests aapki machine par chalte hain** (Flask backend + Appium + phones). Vercel tests nahi chala sakta.
- UI (Vercel) → aapki machine ke backend se **tunnel** ke through baat karti hai.

```
[ Vercel : UI ]  --(internet)-->  [ tunnel ]  -->  [ aapki machine: Flask + Appium + phones ]
```

---

## 1. Vercel account banao (ek baar)
1. https://vercel.com par jao → **Sign Up**
2. GitHub / Google / Email se signup (free "Hobby" plan kaafi hai)

---

## 2. Vercel CLI install karo (ek baar)
Terminal (PowerShell) me:
```
npm i -g vercel
```
Check: `vercel --version` (koi version number aana chahiye)

---

## 3. UI deploy karo
```
cd "C:\Users\Kuldeep Sachan\Documents\Mobile App Testing Framework\lunaPytestBdd\dashboard"
vercel login
```
- Browser khulega → apne account se login karo → terminal me "success"

Phir:
```
vercel --prod
```
Ye kuch sawaal poochega — aise jawaab do:
| Sawaal | Jawaab |
|---|---|
| Set up and deploy? | **Y** |
| Which scope? | apna account chuno |
| Link to existing project? | **N** |
| Project name? | `luna-dashboard` (ya kuch bhi) |
| In which directory is your code? | `./` (Enter) |
| Override settings? | **N** |

Deploy hone ke baad ek **Production URL** milega, jaise:
```
https://luna-dashboard.vercel.app
```
(`.vercelignore` ki wajah se sirf `index.html` upload hoga — `app.py`/config public nahi honge.)

---

## 4. Apni machine par backend + tunnel chalao
**(a) Backend:**
```
run_dashboard.bat        (Flask -> http://127.0.0.1:5000)
```
**(b) Tunnel — cloudflared install (ek baar):**
```
winget install --id Cloudflare.cloudflared
```
(install ke baad naya terminal kholo)

**(c) Tunnel start:**
```
cloudflared tunnel --url http://localhost:5000
```
Ye ek public URL dega, jaise:
```
https://blue-sky-1234.trycloudflare.com
```

---

## 5. Vercel UI ko backend se jodo
Browser me apna Vercel URL is tarah kholo (peeche `?api=` + tunnel URL):
```
https://luna-dashboard.vercel.app/?api=https://blue-sky-1234.trycloudflare.com
```
- Ek baar khola → browser localStorage me yaad rakh lega
- CORS already ON hai, to cross-connect chal jaayega

Ab koi bhi (office me) sirf **Vercel URL** khole → aapki machine ke phones par test chalega.

---

## 6. Rozana use / permanent URL
- **trycloudflare URL har baar badalta hai** (temporary). Har naye tunnel ke baad `?api=` naye URL se dubara kholna hoga.
- **Permanent chahiye** to: Cloudflare account + **named tunnel** (ek fixed URL) — thoda extra one-time setup. Tab `?api=` fix ho jaayega.

---

## 7. Zaroori baatein
- **Aapki machine ON honi chahiye** (backend + tunnel + phones chalte hue) — warna Vercel page khulega par "Run" kaam nahi karega.
- **Security:** public URL par login nahi hai — jiske paas link, wo test trigger kar sakta hai. Trusted logon ko hi do, kaam ke baad tunnel band karo (Ctrl+C). Org ke liye login/password add karwa lena.

---

## Quick recap
1. `npm i -g vercel` → `vercel login` → `cd dashboard` → `vercel --prod`  → Vercel URL
2. `run_dashboard.bat` + `cloudflared tunnel --url http://localhost:5000` → tunnel URL
3. `https://<vercel-url>/?api=https://<tunnel-url>` kholo → done
