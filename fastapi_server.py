# -*- coding: utf-8 -*-
from fastapi import FastAPI, Request
import sqlite3
import uvicorn

# ----------------------
# github 닉네임과 dicord 닉네임(실제 이름) 매핑하기
# ----------------------
github_to_discord = {
    "WhaleliveinCosmos": "황준호",
}

# ----------------------
# DB 초기화
# ----------------------
conn = sqlite3.connect("attendance.db", check_same_thread=False)
c = conn.cursor()
c.execute("""
CREATE TABLE IF NOT EXISTS attendance (
    username TEXT,
    date TEXT
)
""")
conn.commit()

# ----------------------
# FastAPI 서버 설정
# ----------------------
app = FastAPI()

@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()
    if data.get("action") == "opened":
        github_username = data["pull_request"]["user"]["login"]
        discord_nick = github_to_discord.get(github_username, github_username)  # 매핑 없으면 GitHub username 그대로
        date = data["pull_request"]["created_at"].split("T")[0]
        c.execute("INSERT INTO attendance VALUES (?, ?)", (discord_nick, date))
        conn.commit()
        print(f"[Webhook] {discord_nick} 출석 기록 ({date})")
    return {"status": "ok"}

# ----------------------
# 서버 실행
# ----------------------
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
