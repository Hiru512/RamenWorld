'''라이브러리 import
        *의미*'''
import os
import discord #discord -> 디스코드 API 연결용
from discord.ext import commands #commands -> 명령어 시스템(!hello) 쉽게 만들기
from ramen_data import ramen_data


'''intents (핵심개념)
        *구조*
디스코드 ->  "어떤 정보까지 볼 수 있게 할지" 제한됨'''
intents = discord.Intents.default() #default() -> 기본 권한 
intents.message_content = True # message_content = True -> 메시지 내용 읽기 허용


'''봇 생성
        *의미*'''
bot = commands.Bot(command_prefix="!", intents=intents)
#command_prefix="!" -> !hello 이런 식으로 명령어 시작
#intents -> 아까 설정한 권한 적용


'''on_ready(이벤트)
        *구조*
        봇 실행 완료 -> 이벤트 발생 -> 함수 실행
        *역할*
        - 봇 로그인 확인
        - 디버깅용(정상 작동 체크)'''
'''@bot.event
async def on_ready():
    print(f"로그인 완료: {bot.user}")'''

@bot.event
async def on_ready():
    print(f"로그인 완료: {bot.user}")
    print("등록된 명령어:", [cmd.name for cmd in bot.commands])

    '''on_message'''
@bot.event
async def on_message(message):
    if message.author.bot:      #자기 자신 무시 -> 봇끼리 무한루프 방지
        return
    
    await bot.process_commands(message)


def create_ramen_command(ramen_type):
    async def command(ctx):
        shops = ramen_data[ramen_type]
        names = [shop["name"] for shop in shops]

        if names:
            msg = "\n".join(names)
            await ctx.send(f"🍜 {ramen_type} 라멘 리스트: \n{msg}")
        else:
            await ctx.send(f"🍜 {ramen_type} 라멘집 정보가 없습니다.")
    return command
    
for ramen_type in ramen_data.keys():
    bot.command(name=f"{ramen_type}라멘")(create_ramen_command(ramen_type))


'''명령어 만들기
        *구조*'''
@bot.command()      # @bot.comand() -> "이건 명령이다" 표시
async def 라멘(ctx, *, name):
    for shops in ramen_data.values():
        for shop in shops:
            if shop["name"] == name:
                msg = f"""'''yam1
                    🍜{shop['name']}
                    영업시간: {shop['Hours']}
                    브레이크타임: {shop['Breaktime']}
                    라스트오더: {shop['L.O']}
                    캐치테이블: {shop['Catchtable']}
                    인스타그램: {shop['Instagram']}
                    '''"""
                      # ctx (context) -> 누가, 어디서, 어떤 메시지 보냈는지 정보
                await ctx.send(msg)     # await ctx.send() -> 디스코드 채팅으로 메시지 보내기
                return
    await ctx.send("해당 라멘집이 없습니다. 추후 업데이트 될 예정입니다.")


@bot.command()
async def woongseong(ctx):
    await ctx.send("웅성!")

    
    ###print(message.content)      #터미널에서 메시지 출력
    ###await bot.process_commands(message)     #이거 없으면 명령어 시스템 꺼짐

#역할 1: 모든 메시지 들어올 때마다 실행됨


bot.run(os.getenv("DISCORD_TOKEN"))
