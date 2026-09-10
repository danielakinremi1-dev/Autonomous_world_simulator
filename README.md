# AI World Simulator

A Python-based autonomous world simulation where NPCs move, gather resources, manage needs, craft items, trade, and perform role-specific behaviors inside a tile-based world. This was made for fun and practice using conditional logic.

## Features

- Tile-based world with terrain, resources, and obstacles
- NPC roles including villagers, hunters, bakers, nurses, and blacksmiths
- BFS pathfinding and movement
- Local NPC perception/worldview
- Hunger, health, sleeping, and busy states
- Resource gathering with tool durability
- Crafting and item inventories
- Basic buying and selling between NPCs
- Terminal-based world rendering with emojis

## Project Structure 

- `World` — map state, movement, spawning, resources, and interactions
- `NPC` — decision-making, goals, pathfinding, and role behavior
- `Tile` / `Terrain` — environmental state
- `Item` — equipment, resources, durability, and crafting data
- `Renderer` — terminal visualization
- `Simulator` — world tick loop

## Running 