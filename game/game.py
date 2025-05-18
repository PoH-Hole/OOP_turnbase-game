import random

MAX_LEVEL = 90

class Character:
    def __init__(self, name, level=1, exp=0, max_hp=1200, atk=300, defense=100, spd=110,
                 crit_rate=0.1, crit_dmg=0.5, healing_bonus=0.2, heal_items=1):
        self.name = name
        self.level = level
        self.exp = exp
        self.exp_to_next = 100
        self.max_hp = max_hp
        self.hp = max_hp
        self.atk = atk
        self.defense = defense
        self.spd = spd
        self.crit_rate = crit_rate
        self.crit_dmg = crit_dmg
        self.healing_bonus = healing_bonus
        self.heal_items = heal_items

    def print_stats(self):
        print(f"{self.name} (Lvl {self.level}) HP: {self.hp}/{self.max_hp} | ATK: {self.atk} | DEF: {self.defense} | SPD: {self.spd} | EXP: {self.exp}/{self.exp_to_next} | Heals: {self.heal_items} | CRIT Rate: {self.crit_rate * 100:.1f}% | CRIT Damage: {self.crit_dmg * 100:.1f}% | Healing Bonus: {self.healing_bonus * 100:.1f}%")

    def level_up(self):
        if self.level >= MAX_LEVEL:
            return
        self.level += 1
        self.exp_to_next = int(self.exp_to_next * 1.15)
        self.max_hp = int(self.max_hp * 1.08)
        self.atk = int(self.atk * 1.08)
        self.defense = int(self.defense * 1.08)
        self.crit_rate = min(self.crit_rate + 0.01, 1.0)
        self.crit_dmg = min(self.crit_dmg + 0.45, 45.0)
        self.healing_bonus = min(self.healing_bonus + 4, 400.0)
        self.hp = self.max_hp
        print(f"\n*** {self.name} leveled up to {self.level}! ***")
        self.print_stats()

    def gain_exp(self, amount):
        if self.level >= MAX_LEVEL:
            return
        self.exp += amount
        print(f"{self.name} gains {amount} EXP.")
        while self.exp >= self.exp_to_next and self.level < MAX_LEVEL:
            self.exp -= self.exp_to_next
            self.level_up()

    def heal(self):
        if self.heal_items > 0:
            heal_amt = int(300 * (1 + self.healing_bonus))
            self.hp = min(self.max_hp, self.hp + heal_amt)
            self.heal_items -= 1
            print(f"{self.name} heals for {heal_amt}! (HP: {self.hp}/{self.max_hp})")

    def auto_heal(self):
        if self.hp < self.max_hp // 2 and self.heal_items > 0:
            self.heal()

def scaled_enemy(battle_num):
    base_hp = 1000 + (battle_num * 80)
    base_atk = 300 + (battle_num * 29.30)
    base_defense = 120 + (battle_num * 7.5)
    base_spd = 100 + (battle_num // 10)

    max_fluctuation = 0.1 
    hp_variation = random.uniform(-max_fluctuation, max_fluctuation)
    atk_variation = random.uniform(-max_fluctuation, max_fluctuation)
    def_variation = random.uniform(-max_fluctuation, max_fluctuation)
    spd_variation = random.uniform(-max_fluctuation, max_fluctuation)

    return Character(
        name=f"Kroco ke-{battle_num}",
        level=min(1 + battle_num // 5, 80),
        max_hp=int(base_hp * (1 + hp_variation)),
        atk=int(base_atk * (1 + atk_variation)),
        defense=int(base_defense * (1 + def_variation)),
        spd=int(base_spd * (1 + spd_variation)),
        crit_rate=0.1 + min(0.25, battle_num * 0.002),
        crit_dmg=0.4 + min(0.45, battle_num * 0.0045),
        healing_bonus=0,
        heal_items=0
    )

def final_boss(player):
    return Character(
        name="Final Boss: Flame Reaver",
        level=MAX_LEVEL,
        max_hp=player.max_hp * 80,
        atk=int(player.atk *0.8),
        defense=int(player.defense *1.2),
        spd=int(player.spd * 0.8),
        crit_rate=0.2,
        crit_dmg=1.5,
        healing_bonus=0.1,
        heal_items=0
    )

def calculate_damage(attacker, defender):
    base = attacker.atk - defender.defense
    if base < 0:
        base = 0
    if random.random() < attacker.crit_rate:
        print("** CRITICAL HIT! **")
        return int(base * (1 + attacker.crit_dmg))
    return base

def battle(player, enemy, reward_exp=500, drop_chance=2.25):
    print(f"\n--- BATTLE: {player.name} vs {enemy.name} ---")
    turn = [player, enemy] if player.spd >= enemy.spd else [enemy, player]

    while player.hp > 0 and enemy.hp > 0:
        for actor in turn:
            if actor.hp <= 0:
                continue
            if actor == player:
                player.auto_heal()
            target = enemy if actor == player else player
            dmg = calculate_damage(actor, target)
            target.hp = max(0, target.hp - dmg)
            print(f"{actor.name} hits {target.name} for {dmg} damage! (HP: {target.hp}/{target.max_hp})")
            if target.hp == 0:
                break

    if player.hp > 0:
        print(f"\n{player.name} defeated {enemy.name}!")
        player.gain_exp(reward_exp)
        if random.random() < drop_chance:
            player.heal_items += 1
            print(f"{player.name} found a healing item! (Total: {player.heal_items})")
        return True
    else:
        print(f"\n--- {player.name} was defeated... GAME OVER ---")
        return False

def main():
    player = Character("The Herta")
    battle_count = 0

    while player.hp > 0:
        battle_count += 1

        if player.level >= MAX_LEVEL:
            print("\n>>> Final Battle Unlocked! <<<")
            boss = final_boss(player)
            if battle(player, boss, reward_exp=0, drop_chance=0):
                print("\n=== YOU HAVE DEFEATED THE FINAL BOSS. VICTORY! ===")
            break

        print(f"\n[ BATTLE ke-{battle_count} ]")
        enemy = scaled_enemy(battle_count)
        reward_exp = 500 + battle_count * 15
        if battle(player, enemy, reward_exp=reward_exp, drop_chance=0.4):
            print(f"\n--- Status after battle ke-{battle_count} ---")
            player.print_stats()
        else:
            break

    if player.hp <= 0:
        print(f"\n=== Game Over after {battle_count} battles. ===")

if __name__ == "__main__":
    main()