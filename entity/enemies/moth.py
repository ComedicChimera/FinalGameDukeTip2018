from entity.entity import Entity
from util import Point2D
from render.sprite import AnimatedSprite
from random import randint, choice


class Moth(Entity):
    def __init__(self, x, y):
        super().__init__(Point2D(x, y), 5, False, AnimatedSprite('moth.png', Point2D(64, 64), 8), 60, 25, enemy=True)
        self.moving_random = 0
        self.random_direction = (0, 0)

    def update(self, player_pos):
        if self.moving_random > 0:
            self.move_random()
        elif randint(0, 5) == 0:
            self.random_direction = (choice([-2, 2]), choice([-2, 2]))
            self.move_random()
        else:
            self.transform(x=1 if player_pos.x > self.position.x else -1, y=1 if player_pos.y > self.position.y else -1)

        super().update()

    def move_random(self):
        if self.moving_random == 5:
            self.moving_random = 0
        else:
            self.moving_random += 1
        self.transform(x=self.random_direction[0], y=self.random_direction[1])

