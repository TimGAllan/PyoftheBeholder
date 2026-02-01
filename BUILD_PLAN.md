# Eye of the Beholder Remake - Build Plan

## Current State

**Already Implemented:**
- Viewport rendering with 33-panel depth system
- Player movement & rotation (WASD, Q/E)
- Dungeon structure (wall grids, clipping)
- Switch/lever interaction (1 working lever)
- Adornment system
- Basic UI overlay (compass)
- Asset loading from sprite sheets

---

## Build Plan

### Phase 1: Core RPG Foundation

**1.1 Character System**
- `Class_Character.py` - Stats (STR, INT, WIS, DEX, CON, CHA), HP, AC, level, XP
- Support for 4 race types (Human, Elf, Dwarf, Halfling)
- Support for 4 class types (Fighter, Mage, Cleric, Thief)
- Party system (4-character party like original EOB)

**1.2 Inventory System**
- `Class_Item.py` - Item base class with type, weight, effects
- `Class_Inventory.py` - Per-character inventory grid (like original)
- Equipment slots (weapon, armor, helmet, shield, etc.)
- Item pickup/drop mechanics

**1.3 Save/Load System**
- Serialize game state (party, dungeon progress, switches)
- JSON or pickle-based persistence

---

### Phase 2: Combat System

**2.1 Monster Framework**
- `Class_Monster.py` - HP, AC, damage, behavior, sprite
- Monster placement in dungeon data
- Monster movement AI (patrol, chase, flee)

**2.2 Combat Mechanics**
- Turn-based or real-time with pause (EOB was real-time)
- Attack rolls using D&D-style mechanics
- Damage calculation with weapon/armor modifiers
- Death and party wipe handling

**2.3 Combat UI**
- Click-to-attack on viewport
- Health bars for party members
- Combat log/message area

---

### Phase 3: Magic System

**3.1 Spell Framework**
- `Class_Spell.py` - Spell definitions (name, level, effect, cost)
- Spell books for Mages/Clerics
- Memorization system (rest to prepare spells)

**3.2 Spell Effects**
- Damage spells (Fireball, Magic Missile)
- Healing spells (Cure Light Wounds)
- Buff/debuff spells (Bless, Hold Person)
- Utility spells (Detect Magic, Light)

**3.3 Spell UI**
- Spell selection interface
- Casting animations/effects on viewport

---

### Phase 4: Advanced Dungeon Features

**4.1 Interactive Elements**
- Pressure plates (trigger on step)
- Teleporters
- Pits (falling damage, level transitions)
- Secret doors (search mechanic)
- Locked doors (keys, lockpicking)

**4.2 Traps**
- Dart traps, spike traps, poison gas
- Trap detection (Thief skill)
- Trap disarming

**4.3 Multi-Level Dungeons**
- Stairs up/down transitions
- Level 2+ dungeon data files
- Different environments (Sewer → Crypt → Castle, etc.)

---

### Phase 5: UI & Polish

**5.1 Full UI Implementation**
- Character stat panels (clickable portraits)
- Inventory grid UI
- Spell book interface
- Main menu (New Game, Load, Options)
- Pause menu

**5.2 Audio**
- Background music (ambient dungeon tracks)
- Sound effects (footsteps, combat, doors, spells)
- UI sounds (clicks, inventory)

**5.3 Visual Polish**
- Monster sprites in viewport
- Spell effect animations
- Damage indicators
- Torch/lighting flicker effect

---

### Phase 6: Content & Balance

**6.1 Dungeon Content**
- Design 12+ dungeon levels (like original EOB)
- Place monsters, treasures, secrets
- Create puzzles and key progression

**6.2 Items & Loot**
- Weapons (swords, axes, bows, daggers)
- Armor sets
- Potions, scrolls, wands
- Quest items and keys

**6.3 Balancing**
- XP curves and leveling
- Monster difficulty scaling
- Loot distribution

---

## Suggested File Structure

```
POB/
├── Main.py
├── Class_Game.py
├── Class_Player.py          (expand for party management)
├── Class_Character.py       [NEW]
├── Class_Party.py           [NEW]
├── Class_Monster.py         [NEW]
├── Class_Item.py            [NEW]
├── Class_Inventory.py       [NEW]
├── Class_Spell.py           [NEW]
├── Class_Combat.py          [NEW]
├── Class_Dungeon.py
├── Class_DungeonView.py
├── Class_DungeonTileSet.py
├── Class_UI.py              [NEW]
├── Class_SaveLoad.py        [NEW]
├── dungeons/
│   ├── level_01_sewer.py
│   ├── level_02_crypt.py
│   └── ...
└── data/
    ├── monsters.json        [NEW]
    ├── items.json           [NEW]
    └── spells.json          [NEW]
```

---

## Recommended Build Order

| Priority | System | Reason |
|----------|--------|--------|
| 1 | Character/Party | Foundation for all RPG mechanics |
| 2 | Inventory/Items | Enables equipment and loot |
| 3 | Monsters (no combat) | Populate dungeon visually |
| 4 | Combat | Core gameplay loop |
| 5 | Save/Load | Playability milestone |
| 6 | Magic | Expands combat options |
| 7 | Advanced dungeon | Puzzles and variety |
| 8 | Audio | Atmosphere |
| 9 | Content | Full game experience |
