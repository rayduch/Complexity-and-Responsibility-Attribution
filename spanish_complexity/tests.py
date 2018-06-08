from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants


class PlayerBot(Bot):

    def play_round(self):
        yield (pages.SwitchRoles)
        yield (pages.Intro)
        yield (pages.Intro2)
        yield (pages.P1Instructions)
        yield (pages.P2Instructions)
        yield (pages.Quiz)
        yield (pages.P2FirstDecision,{'retaining':4})
        yield (pages.P1Decision{'task1decision':1,'task2decision':1})
        yield (pages.P2SecondDecision{'task1guess':1, 'task2guess':0})
        yield (pages.BeforeOutcomeWP)
        yield (pages.Outcome)
        yield (pages.FinalResults)
        yield (pages.ShuffleWaitPage)




