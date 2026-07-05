# 🧾 Git Cheat-Sheet (Hinglish) — Luna project

Saari git commands, unka use, aur examples — ek jagah. ⭐ = roz kaam aane wali.

---

## 🧠 0. Git kaise sochta hai (4 jagah)
```
[1 Working folder]  →(git add)→  [2 Staging]  →(git commit)→  [3 Local history]  →(git push)→  [4 GitHub]
   aapki files        bhejne ke liye chuni       save-point (snapshot)              internet par copy
                      hui files
```
- **git add** = files ko "bhejne ke liye" chuno (staging)
- **git commit** = snapshot/save-point banao (local)
- **git push** = GitHub par upload
- **git pull** = GitHub se latest wapas lao

---

## ⚙️ 1. Setup (ek baar)
| Command | Kya karta hai |
|---|---|
| `git config --global user.name "Naam"` | Aapka naam (commits par lagta hai) |
| `git config --global user.email "email"` | Aapka email |
| `git init` | Kisi folder ko **git repo banao** (`.git` banta hai) |
| `git clone <url>` | GitHub se **poori repo download** karo (naye PC par) |

---

## 🔁 2. Roz ka kaam ⭐ (90% yahi)
| Command | Kya karta hai |
|---|---|
| `git status` ⭐ | Kya badla / naya / staged hai — **hamesha pehle ye** |
| `git add .` ⭐ | **Saari** changes stage karo |
| `git add <file>` | Sirf **ek file** stage karo |
| `git commit -m "msg"` ⭐ | Staged changes ka **snapshot** save |
| `git push` ⭐ | Commits **GitHub par upload** |
| `git pull` ⭐ | GitHub se **latest** wapas lao |

**Daily flow:** `git status` → `git add .` → `git commit -m "..."` → `git push`

**Example:**
```
$ git status
  modified:   pages/sleep_page.py
$ git add .
$ git commit -m "sleep page fix"
[master 3f9a1c2] sleep page fix
 1 file changed, 14 insertions(+)
$ git push
   7a5274d..3f9a1c2  master -> master
```

---

## 🔍 3. Dekhna / inspect
| Command | Kya karta hai |
|---|---|
| `git log --oneline` | Commits ki chhoti list (history) |
| `git log` | Poori detail history |
| `git diff` | Jo abhi tak commit nahi hua, wo kya badla |
| `git show <commit-id>` | Ek commit me kya change hua |
| `git remote -v` | Konsi GitHub repo se juda hai (URL) |
| `git branch` | Saari branches (jahan ho `*` se) |

---

## 🌐 4. Remote / GitHub se jodna
| Command | Kya karta hai |
|---|---|
| `git remote add origin <url>` | Local repo ko **GitHub repo se jodo** (`origin` = uska naam) |
| `git push -u origin main` | **Pehli baar** push + track set (aage sirf `git push`) |
| `git remote -v` | Jud a URL dekho |
| `git remote remove origin` | Galat URL hatao |
| `git fetch` | GitHub se changes laao **par merge mat karo** |

---

## 🌿 5. Branch (alag-alag version me kaam)
**Branch = code ki alag copy.** `master`/`main` safe rakhte hue nayi branch par experiment.

| Command | Kya karta hai |
|---|---|
| `git branch` | Branches ki list |
| `git switch -c <naam>` | Nayi branch banao **aur** uspe jao |
| `git switch <naam>` | Us branch par jao *(purana: `git checkout <naam>`)* |
| `git merge <naam>` | Us branch ka code current branch me **milao** |
| `git branch -d <naam>` | Branch **delete** (merge ho chuki ho) |
| `git push -u origin <naam>` | Branch ko **GitHub par bhejo** |
| `git branch -M main` | Current branch ka naam `main` karo |

---

## ↩️ 6. Galti sudharo (undo) — dhyaan se
| Command | Kya karta hai |
|---|---|
| `git restore <file>` | File ki **un-committed changes hatao** (wapas purani) |
| `git restore --staged <file>` | `git add` **undo** (unstage), change rehta hai |
| `git reset --soft HEAD~1` | Aakhri commit hatao **par changes rakho** |
| `git reset --hard HEAD~1` | ⚠️ Aakhri commit **+ changes dono** hatao (khatarnak) |
| `git revert <commit-id>` | Kisi commit ko ulta karne wala **naya** commit (safe) |

---

## 🚫 7. `.gitignore` (file — command nahi)
Ek file jisme likhte ho **kaunsi cheezein git track NA kare**. Zaroori — secrets/bhaari folders yahan daalo:
```
.env
myenv/
venv/
_output/
allure-results/
allure-report/
__pycache__/
*.pyc
```

---

## 🎬 8. Real-life flows (commands mila ke)

### A) Pehli baar project GitHub par daalna
```
git init
git add .
git commit -m "first commit"
git branch -M main
git remote add origin <url>
git push -u origin main
```

### B) Baad me change karke update ⭐ (roz)
```
git add .
git commit -m "kya change kiya"
git push
```

### C) GitHub se local par laana (naya PC)
```
git clone <url>
cd <repo-folder>
```

### D) Latest lana (repo pehle se local)
```
git pull
```

### E) Clone → kaam → wapas push (poora)
```
git clone <url>
cd <repo>
git pull                 # latest
# ...files edit...
git add .
git commit -m "change"
git push
```

### F) Branch banane se master + GitHub tak (poora)
```
git switch master
git pull                       # latest lo
git switch -c feature-x        # nayi branch + uspe jao
# ...kaam + commit...
git add .
git commit -m "feature x"
git push -u origin feature-x   # (chaho to) branch GitHub par
git switch master              # master par wapas
git merge feature-x            # code master me le aao
git push                       # master GitHub par update
git branch -d feature-x        # branch delete
```

---

## ❓ 9. 2 common sawaal

**Q1: Dusri branch par kaam kiya — push ke liye master par aana zaroori?**
> **Nahi.** `git push` **jis branch par ho wahi** bhejta hai. Sirf branch bhejni ho: `git push -u origin <branch>` (master ki zaroorat nahi). Code **master me** chahiye tabhi merge karo.

**Q2: Dusri branch ka saara code master me kaise?**
```
git switch master
git merge <branch-naam>
git push
```

---

## 🧭 10. Quick reference (sab ek nazar me)
| Kaam | Command |
|---|---|
| Kya badla | `git status` |
| Ready karo | `git add .` |
| Save | `git commit -m "msg"` |
| GitHub bhejo | `git push` |
| Latest lao | `git pull` |
| Download (naya PC) | `git clone <url>` |
| Branches | `git branch` |
| Nayi branch + jao | `git switch -c <naam>` |
| Branch badlo | `git switch <naam>` |
| Merge | `git merge <naam>` |
| Branch delete | `git branch -d <naam>` |
| Branch GitHub bhejo | `git push -u origin <naam>` |
| History | `git log --oneline` |
| Undo file | `git restore <file>` |

---

## ⚠️ 11. Push se pehle SECURITY (framework ke liye)
- `.env` (DB/email passwords), `myenv/`, `venv/`, `_output/` **GitHub par NA jaayein** → `.gitignore` me daalo.
- `.env` agar pehle se commit ho chuki ho: `git rm --cached .env` → commit. Repo **Private** rakho.

---

## 🔑 Sirf itna yaad rakho (90% kaam)
```
git status   → kya badla dekho
git add .    → sab ready
git commit -m "..."  → save
git push     → GitHub bhejo
git pull     → latest lao
```

*Cheat-sheet — Luna project. Kabhi bhool jao to yahi khol lena.* 🙂
