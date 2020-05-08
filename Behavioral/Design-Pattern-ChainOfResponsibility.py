
# A Chain of components who all get a chance to process a command or a query , optionally having a default processing implementation
# and an ability to terminate the processing chain

class Creature:
    def __init__(self, name, attack, defense):
        self.defense = defense
        self.attack = attack
        self.name = name

    def __str__(self):
        return f'{self.name} ({self.attack}/{self.defense})'


class CreatureModifier:
    def __init__(self, creature):
        self.creature = creature
        self.next_modifier = None
## Everytime I add a modifier I call my next modifier which sets a new next modifier 
## this is how the chaining happens
    def add_modifier(self, modifier):
        if self.next_modifier:
            ## check if I have next modifier I call its add_modifier which takes the flow to the next modifier
            ## and so on unitl we reach the last modifier which does not have next modifier and the execution
            ## goes to the else part of the if condition and all we do it define a next modifer which does not
            ## yet have a next modifier
            self.next_modifier.add_modifier(modifier)
        else:
            self.next_modifier = modifier

    def handle(self):
        ## If I am asked to handle I just call the handle of the next modifier! 
        ## this is how the handles of the next modifiers get chained one after the other
        # until the last modifier that does not have a next modifer and the call to the super handler
        ## does nothing. Note that there is no else statement here which is essential! 
        if self.next_modifier:
            self.next_modifier.handle()


class NoBonusesModifier(CreatureModifier):
    def handle(self):
        print('No bonuses for you!')


class DoubleAttackModifier(CreatureModifier):
    def handle(self):
        print(f'Doubling {self.creature.name}''s attack')
        self.creature.attack *= 2
        super().handle()


class IncreaseDefenseModifier(CreatureModifier):
    def handle(self):
        if self.creature.attack <= 2:
            print(f'Increasing {self.creature.name}''s defense')
            self.creature.defense += 1
        super().handle()


if __name__ == '__main__':
    goblin = Creature('Goblin', 1, 1)
    print(goblin)

    root = CreatureModifier(goblin)

    root.add_modifier(NoBonusesModifier(goblin))

    root.add_modifier(DoubleAttackModifier(goblin))
    root.add_modifier(DoubleAttackModifier(goblin))

    # no effect
    root.add_modifier(IncreaseDefenseModifier(goblin))

    root.handle()  # apply modifiers
    print(goblin)
