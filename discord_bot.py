# -*- coding: utf-8 -*-
import sqlite3
from discord.ext import commands
import discord
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

if TOKEN:
    TOKEN = TOKEN.strip()

if not TOKEN:
    raise RuntimeError("DISCORD_TOKEN 환경변수가 설정되지 않았습니다! .env 또는 서버 환경변수를 확인하세요.")

# ----------------------
# DB 연결
# ----------------------
conn = sqlite3.connect("attendance.db")
c = conn.cursor()

# ----------------------
# Discord 봇 설정
# ----------------------
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="/", intents=intents)

# ----------------------
# 오늘 출석 확인
# ----------------------
@bot.command()
async def 출석확인(ctx):
    c.execute('SELECT DISTINCT username FROM attendance WHERE date = date("now")')
    users = [row[0] for row in c.fetchall()]
    if users:
        await ctx.send(f"오늘의 출석자: {', '.join(users)}")
    else:
        await ctx.send("오늘은 아직 아무도 출석하지 않았어요!")

# ----------------------
# 특정 날짜 출석 확인
# ----------------------
@bot.command()
async def 출석확인날짜(ctx, date: str):
    """
    사용법: /출석확인날짜 2025-10-18
    """
    c.execute('SELECT DISTINCT username FROM attendance WHERE date = ?', (date,))
    users = [row[0] for row in c.fetchall()]
    if users:
        await ctx.send(f"{date} 출석자: {', '.join(users)}")
    else:
        await ctx.send(f"{date}에는 아직 아무도 출석하지 않았어요!")

# ----------------------
# 기간 지정 출석 확인
# ----------------------
@bot.command()
async def 출석조회(ctx, start_date: str, end_date: str):
    """
    사용법: /출석조회 2025-10-01 2025-10-18
    start_date, end_date 형식: YYYY-MM-DD
    """
    c.execute(
        'SELECT DISTINCT username FROM attendance WHERE date BETWEEN ? AND ?',
        (start_date, end_date)
    )
    users = [row[0] for row in c.fetchall()]
    if users:
        await ctx.send(f"{start_date} ~ {end_date} 출석자: {', '.join(users)}")
    else:
        await ctx.send(f"{start_date} ~ {end_date} 기간에는 출석자가 없습니다.")

# ----------------------
# 봇 실행
# ----------------------
bot.run(TOKEN)  # 실제 토큰으로 교체
