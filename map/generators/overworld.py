from map.tile import *
from random import randint, choice
from util import PLAYER_SPAWN, TILE_SIZE
import itertools
from render.sprite import Sprite


# generate standard over world map
def generate_over_world(tiles, top, bottom, x_offset=0, gaps=0, start_height=None):
    gap_locations = []
    if gaps > 0:
        gap_locations = [randint(x_offset, tiles + x_offset) for _ in range(gaps)]
        gap_locations = itertools.chain.from_iterable([[x, x+1] if randint(0, 1) == 0 else [x] for x in gap_locations])
        gap_locations = list(map(lambda x: x * TILE_SIZE, gap_locations))
    prev_height = (top + bottom) // 2
    tile_map = []
    spawned_tree = False
    spawned_pits = 0
    for i in [x for x in range(0, tiles) if x % 2 == 0]:
        x_pos = i * TILE_SIZE + x_offset * TILE_SIZE
        if x_pos in gap_locations and i < tiles - 2 and spawned_pits < 2:
            tile_map.append(Tile(x_pos, TILE_SIZE * 3, *TileSet.SPIKES, 2, collidable=False, damage=100))
            spawned_pits += 1
            continue
        spawned_pits = 0
        height = prev_height + choice([-1, -1, 1, 1, 0])
        height = height if bottom <= height <= top else prev_height
        if start_height:
            height = start_height
            start_height = None
        for _ in range(2):
            if randint(0, 1) == 0:
                tile_map.append(Tile(x_pos, PLAYER_SPAWN + TILE_SIZE * height, *get_decorate_tile(), collidable=False))
            elif randint(0, 4) == 0 and not spawned_tree and prev_height <= height:
                tile_map.append(SpriteTile('tree.png', x_pos - 48,
                                           (PLAYER_SPAWN + TILE_SIZE * height), 128, 128))
                spawned_tree = True
            else:
                spawned_tree = False
            tile_map.append(Tile(x_pos, PLAYER_SPAWN + TILE_SIZE * (height - 1), *TileSet.GRASS))
            if height > 1:
                tile_map.append(Tile(x_pos, PLAYER_SPAWN + TILE_SIZE * (height - 3), *TileSet.DIRT, repeat_y=2))
            if height > 3:
                tile_map.extend([Tile(x_pos, PLAYER_SPAWN, *TileSet.STONE, repeat_y=height - 3)])
            x_pos += TILE_SIZE
        prev_height = height
    return tile_map


def generate_cave_entrance():
    base = 7
    tile_map = []
    for i in range(0, 15):
        if i < 5:
            floor = base - (i - 1 if i > 3 else i)
            floor_stone = TileSet.STONE if i < 3 else TileSet.GLOOM_STONE
            tile_map.append(
                Tile((80 + i) * TILE_SIZE, 0, *floor_stone, repeat_y=floor, collidable=i < 3, render_first=not i < 3))
            if i > 0:
                cave_height = randint(5, 6)
                tile_map.extend([
                    Tile((80 + i) * TILE_SIZE, (floor + cave_height) * TILE_SIZE, *TileSet.STONE, repeat_y=i * 2),
                    Tile((80 + i) * TILE_SIZE, ((floor + cave_height) + i * 2) * TILE_SIZE, *TileSet.SNOW_STONE)
                ])
            if randint(0, 2) == 0 and i < 3:
                tile_map.append(Tile((80 + i) * TILE_SIZE, floor * TILE_SIZE, *TileSet.STALAGMITE, collidable=False))
        else:
            tile_map.extend([
                Tile((80 + i) * TILE_SIZE, 0, *TileSet.STONE, repeat_y=base + i * 2 + 2),
                Tile((80 + i) * TILE_SIZE, (base + i * 2 + 2) * TILE_SIZE, *TileSet.SNOW_STONE)
            ])
    return tile_map


def get_decorate_tile():
    if randint(0, 4) == 0:
        return choice([
            TileSet.GRASS_SURFACE,
            TileSet.PINK_FLOWER,
            TileSet.YELLOW_FLOWER,
            TileSet.MOSSY_LOG,
            TileSet.LOG
        ])
    else:
        return TileSet.GRASS_SURFACE