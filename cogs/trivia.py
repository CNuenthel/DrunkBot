import asyncio

import discord
from discord.ext import commands
import requests
import html
from dataclasses import dataclass
import random


@dataclass
class Player:
    name: str
    score: int
    guessed: bool


class Trivia:
    def __init__(self):
        self.api_route = "https://opentdb.com/api.php?amount=10&type=multiple"
        self.questions = []

    def request_questions(self):
        response = requests.get(self.api_route)

        if response.status_code == 200:
            self.questions = response.json()["results"]

        else:
            print("Failed to contact Trivia API", response.status_code)

    def get_question(self):
        if self.questions:
            question_data = self.questions[0]
            self.questions.remove(question_data)
            return self.format_question_data(question_data)
        return None

    @staticmethod
    def format_question_data(question_data: dict):
        for k, v in question_data.items():
            question_data[k] = html.unescape(v)
        return question_data


class Triviacog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Triviacog is Ready!")

    @commands.command(aliases=["Meh"])
    async def trivia(self, ctx):
        triv = Trivia()
        triv.request_questions()

        if not triv.questions:
            await ctx.send("Oh sorry... something went wrong")
            return

        trivia_start_em = discord.Embed(
            title="Drunk Trivia",
            description="Trivia for the Drunk Hoes and Bros",
            color=discord.Color.purple()
        )
        trivia_start_em.set_author(
            name="Trivia",
            icon_url="https://mpng.subpng.com/20190723/arf/kisspng-portable-network-graphics-trivia-computer-"
                     "icons-qu-web-dev-5d37661d0a0037.775050221563911709041.jpg"
        )
        trivia_start_em.add_field(
            name="Trivia Starting",
            value="React to this message to join Trivia!",
            inline=False
        )

        trivia_start_msg = await ctx.send(embed=trivia_start_em)

        emojis = ["🧠", "🍆", "🎲"]
        await trivia_start_msg.add_reaction(random.choice(emojis))

        def check(reaction, member):
            pass

        try:
            reaction, member = await self.bot.wait_for(event='reaction_add', check=check, timeout=60.0)
        except asyncio.TimeoutError:
            pass

x = Trivia()
x.request_questions()
print(x.get_question())

# {
#     "category": "category",
#     "type": "multiple",
#     "difficulty": "difficulty",
#     "question": "question text",
#     "correct_answer": "correct_answer",
#     "incorrect_answers": ["in_ans", "in_ans", "in_ans"]
# }


def setup(bot):
    bot.add_cog(Triviacog(bot))