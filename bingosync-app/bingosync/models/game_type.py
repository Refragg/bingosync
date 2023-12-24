from enum import Enum, unique

@unique
class GameType(Enum):
    custom = 1
    custom_randomized = 2
    custom_srl_v5 = 3
    custom_isaac = 4
    sonic_adventure_dx = 5
    sonic_adventure_2 = 6
    sonic_adventure_2_hero_story = 7
    sonic_adventure_2_dark_story = 8
    sonic_adventure_2_long = 9
    sonic_adventure_2_nightmare = 10
    sonic_r_regular = 11
    sonic_r_balanced = 12
    shadow_normal = 13
    shadow_hero = 14
    shadow_dark = 15
    shadow_vs = 16
    billy = 17


    def __str__(self):
        return self.short_name

    @property
    def group(self):
        return GAME_TYPE_GROUPS[self]

    @property
    def group_name(self):
        return GAME_TYPE_GROUP_NAMES[self]

    @property
    def long_name(self):
        return GAME_TYPE_LONG_NAMES[self]

    @property
    def short_name(self):
        return GAME_TYPE_SHORT_NAMES[self]

    @property
    def variant_name(self):
        return GAME_TYPE_VARIANT_NAMES[self]

    @property
    def is_game_group(self):
        return self.group == self

    @property
    def is_custom(self):
        return self in (GameType.custom, GameType.custom_randomized, GameType.custom_srl_v5, GameType.custom_isaac)

    @property
    def uses_seed(self):
        # fixed custom is the one game type that doesn't use a seed
        return self != GameType.custom

    @staticmethod
    def for_value(value):
        return list(GameType)[value - 1]

    def generator_instance(self):
        from bingosync.generators import BingoGenerator, CustomGenerator
        if self.is_custom:
            return CustomGenerator(self)
        else:
            return BingoGenerator.instance(self.name)

    @staticmethod
    def choices():
        return [(game_type.value, game_type.long_name) for game_type in GameType]

    @staticmethod
    def game_choices():
        choices = [(gt.value, gt.group_name) for gt in GAME_GROUPS if gt.is_game_group and not gt.is_custom]
        choices = list(sorted(choices, key=lambda el: strip_articles(el[1]).lower()))
        custom_choices = [(gt.value, gt.group_name) for gt in [GameType.custom]]
        return [(None, '')] + choices + custom_choices

    @staticmethod
    def variant_choices():
        return [(group_gt.value,
                 [(gt.value, name) for gt, name, short_name in group['variants'] if gt not in HIDDEN_VARIANTS])
                for group_gt, group in GAME_GROUPS.items()]

def strip_articles(name):
    """A hacky sort key that ignores things like 'The ' """
    if name.startswith("The "):
        return name[4:]
    elif name.startswith("A "):
        return name[2:]
    return name


DEFAULT_VARIANT_NAME = "Normal"
def singleton_group(game_type, name, short_name=None, variant_name=DEFAULT_VARIANT_NAME):
    if short_name is None:
        short_name = name
    return {
        game_type: {
            "name": name,
            "variants": [
                (game_type, variant_name, short_name),
            ],
        }
    }

# specific game type variants to hide from the variant dropdown as a "soft removal"
# don't actually remove the variant so that it still shows the correct data for historical rooms.
# this will probably break if all of the variants for a game group are hidden.
HIDDEN_VARIANTS = {
}

MANUAL_GAME_GROUPS = {
    GameType.custom: {
        "name": "Custom (Advanced)",
        "variants": [
            (GameType.custom, "Fixed Board", "Custom"),
            (GameType.custom_randomized, "Randomized", "Custom (Rand)"),
            (GameType.custom_srl_v5, "SRL v5", "Custom (SRLv5)"),
            (GameType.custom_isaac, "Isaac", "Custom (Isaac)"),
        ],
    },
    GameType.sonic_adventure_2: {
        "name": "Sonic Adventure 2",
        "variants": [
            (GameType.sonic_adventure_2, "Normal", "SA2"),
            (GameType.sonic_adventure_2_hero_story, "Hero Story", "SA2 Hero"),
            (GameType.sonic_adventure_2_dark_story, "Dark Story", "SA2 Dark"),
            (GameType.sonic_adventure_2_long, "Long", "SA2 Long"),
            (GameType.sonic_adventure_2_nightmare, "Nightmare", "SA2 Nightmare"),
        ],
    },
    GameType.shadow_normal: {
        "name": "Shadow The Hedgehog",
        "variants": [
            (GameType.shadow_normal, "Normal", "Shadow Normal"),
            (GameType.shadow_hero, "Hero", "Shadow Hero"),
            (GameType.shadow_dark, "Dark", "Shadow Dark"),
            (GameType.shadow_vs, "2 vs 2", "Shadow 2 vs 2"),
        ],
    },
    GameType.sonic_r_regular: {
        "name": "Sonic R",
        "variants": [
            (GameType.sonic_r_regular, "Regular", "Sonic R Regular"),
            (GameType.sonic_r_balanced, "Balanced", "Sonic R Balanced"),
        ],
    },
}
SINGLETON_GAME_GROUPS = {
    **singleton_group(GameType.sonic_adventure_dx, "Sonic Adventure DX", "SADX"),
    **singleton_group(GameType.billy, "Billy Hatcher and the Giant Egg", "Billy"),
}
GAME_GROUPS = {**MANUAL_GAME_GROUPS, **SINGLETON_GAME_GROUPS}

GAME_TYPE_GROUPS = {}
GAME_TYPE_GROUP_NAMES = {}
GAME_TYPE_LONG_NAMES = {}
GAME_TYPE_SHORT_NAMES = {}
GAME_TYPE_VARIANT_NAMES = {}
ALL_VARIANTS = []
for group, entry in GAME_GROUPS.items():
    name = entry["name"]
    variants = entry["variants"]
    for game, variant_name, short_name in variants:
        if len(variants) == 1 and variant_name == "Normal":
            long_name = name
        else:
            long_name = name + " - " + variant_name
        GAME_TYPE_GROUPS[game] = group
        GAME_TYPE_GROUP_NAMES[game] = name
        GAME_TYPE_LONG_NAMES[game] = long_name
        GAME_TYPE_SHORT_NAMES[game] = short_name
        GAME_TYPE_VARIANT_NAMES[game] = variant_name
        ALL_VARIANTS.append(game)
