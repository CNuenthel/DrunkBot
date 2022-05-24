import asyncio

import discord
from discord.ext import commands
import requests
import html
from dataclasses import dataclass
import random

TOTAL_PLAYERS = {}


@dataclass
class Player:
    def __init__(self, name: str):
        self.name = name
        self.guessed = False
        self.answer = None
        self.answer_time = 0
        self.score = 0


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


class TriviaBot(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.trivia_started = False
        self.trivia = Trivia()
        self.players = {}
        self.trivmoji = None
        self.trivia_caller = None
        self.player_collection = True
        self.trivia_start_msg = None
        self.question_time_up = False

    @commands.Cog.listener()
    async def on_ready(self):
        print("TriviaBot is Ready!")

    @commands.command(aliases=["Meh"])
    async def trivia(self, ctx):
        if not self.trivia_started:
            self.trivia_started = True
            self.trivia_caller = ctx.message.author.name
            self.players[ctx.message.author.name] = Player(ctx.message.author.name)
            self.trivia.request_questions()

            if not self.trivia.questions:
                await ctx.send("Oh sorry... something went wrong with the TriviaAPI")
                return

            self.trivmoji = random.choice(["🧠", "🍆", "🎲"])

            trivia_start_em = discord.Embed(
                color=discord.Color.purple()
            )
            trivia_start_em.add_field(
                name="Trivia Starting!",
                value=f"{self.trivmoji} to join."
            )
            trivia_start_em.set_author(
                name="Trivia",
                icon_url="https://mpng.subpng.com/20190723/arf/kisspng-portable-network-graphics-trivia-computer-"
                         "icons-qu-web-dev-5d37661d0a0037.775050221563911709041.jpg"
            )
            trivia_start_em.set_footer(text=f"Hey {ctx.message.author.name}, react with ✅ to start!")

            self.trivia_start_msg = await ctx.send(embed=trivia_start_em)

            await self.trivia_start_msg.add_reaction(self.trivmoji)
            await self.trivia_start_msg.add_reaction("✅")

            self.player_collection = True
            await self.collect_players()

    @commands.Cog.listener()
    async def collect_players(self):
        while self.player_collection:
            # TODO change to correct bot name
            def check(reaction, user):
                return str(reaction) in ["✅", self.trivmoji] and user.name != "VolleyBot#2809"

            reaction, user = await self.bot.wait_for("reaction_add", check=check)

            if user.name not in self.players:
                await self.trivia_start_msg.channel.send(f"{user.name}, you are in!")
                self.players[user.name] = Player(user.name)

            elif str(reaction) == "✅" and user.name == self.trivia_caller:
                self.player_collection = False

                await self.trivia_start_msg.channel.send(
                    f"Trivia Beginning!")
                await self.trivia_start_msg.delete()
                await self.trivia_begin()

    async def trivia_begin(self):

        def q_embed(question_number: int, question: str, answers: list):
            embed = discord.Embed(
                title=f"Question {question_number}:",
                description=f"{question}\n"
                            f":one: {answers[0]}\n"
                            f":two: {answers[1]}\n"
                            f":three: {answers[2]}\n"
                            f":four: {answers[3]}"
            )
            embed.set_footer(text="React with your answer!")
            return embed

        self.player_collection = False

        question_number = 1
        while self.trivia.questions:
            self.question_time_up = False
            self.player_answers = {}

            question = self.trivia.get_question()
            question["incorrect_answers"].append(question["correct_answer"])
            random.shuffle(question["incorrect_answers"])
            answers = question["incorrect_answers"]
            correct_index = answers.index(question["correct_answer"])

            while not self.question_time_up:
                question_msg = await self.trivia_start_msg.channel.send(
                    embed=q_embed(question_number, question["question"], answers)
                )

                for reaction in ["1️⃣", "2️⃣", "3️⃣", "4️⃣"]:
                    await question_msg.add_reaction(reaction)

                await self.question_timer()
                await self.collect_answers()

            await self.judge_questions(correct_index)
            self.reset_players()
            question_number += 1

    @commands.Cog.listener()
    async def collect_answers(self):
            # TODO change to correct bot name
        def check(msg):
            print(msg)
            return msg.content in ["1", "2", "3", "4"] \
                   and msg.author.name != "VolleyBot" \
                   and msg.author.name in self.players

        msg = await self.bot.wait_for("message", check=check)


        print(msg.author, msg.content)

        # self.players[user.name].answer = reaction_answers[reaction]
        # self.players[user.name].answer_time = self.timer
        # await self.trivia_start_msg.channel.send(f"{user} picked {reaction}!")

    async def question_timer(self):
        self.timer = 0
        while not self.question_time_up:
            if self.timer < 10:
                await asyncio.sleep(1)
                print(self.timer)
                self.timer += 1
            else:
                self.question_time_up = True

    async def judge_questions(self, correct_answer_index: int):
        answer_embed = discord.Embed(
            title="Times Up"
        )
        for player in self.players:
            if self.players[player].answer is not None:
                if self.players[player] == correct_answer_index:
                    self.players[player].score += 10-self.players[player].answer_time
                    answer_embed.add_field(
                        name=f"{player} guessed {self.players[player]}.",
                        value=f"Time: {self.players[player].answer_time}s\n"
                              f"Got it right!\n"
                              f"Score + {10-self.players[player].answer_time}",
                        inline=True
                    )
                else:
                    answer_embed.add_field(
                        name=f"{player} guessed {self.players[player]}.",
                        value=f"Time: {self.players[player].answer_time}s\n"
                              f"Got it wrong...",
                        inline=True
                    )
            else:
                answer_embed.add_field(
                    name=f"{player} did not make a guess...",
                    value=f"You good bud?",
                    inline=True
                )

        await self.trivia_start_msg.channel.send(embed=answer_embed)

    def reset_players(self):
        for player in self.players:
            self.players[player].guessed = False
            self.players[player].answer = None
            self.players[player].answer_time = 0

# {
#     "category": "category",
#     "type": "multiple",
#     "difficulty": "difficulty",
#     "question": "question text",
#     "correct_answer": "correct_answer",
#     "incorrect_answers": ["in_ans", "in_ans", "in_ans"]
# }


def setup(bot):
    bot.add_cog(TriviaBot(bot))