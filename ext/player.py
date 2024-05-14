import pygame
import math
import pygame.mask
from tiles.collision.col import Collision
from tiles.tile import Tile
from tiles.tiletype import TileType
from tiles.tiles import TILES
from pygame.locals import *


class Player:
    """Player object"""
    def __init__(self, x_pos, y_pos, screen, name: str = "Player"):
        self.name = name
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.screen = screen
        self.velocity_y = 0 
        self.velocity_x = 0

        self.right_leg = pygame.image.load(".\\assets\\textures\\steve\\r_leg.png").convert_alpha()
        self.left_leg = pygame.image.load(".\\assets\\textures\\steve\\l_leg.png").convert_alpha()
        self.torso = pygame.image.load(".\\assets\\textures\\steve\\torso.png").convert_alpha()
        self.hand = pygame.image.load(".\\assets\\textures\\steve\\hand.png").convert_alpha()
        self.head = pygame.image.load(".\\assets\\textures\\steve\\head.png").convert_alpha()
        
        self.gravity = 70
        self.time_passed = 0
        self.fixed_time_step = 0.02 

        self.player_color = (255, 0, 0)
        self.torso_rect = pygame.Rect(self.x_pos, self.y_pos, 16, 24) 
        self.player_rect = self.torso_rect.copy()
        self.legs_rect = None
        self.torso_rect = None
        self.hand_rect = None

        self.player_collision_rect = pygame.Rect(self.x_pos, self.y_pos, 16*3, 48*3)
        self.facing_right = True
        self.speed = 5
        self.isGrounded = False
        
        self.collision = Collision() 
        self.tile = Tile(self.screen, self.screen.get_width(), self.screen.get_height())

        self.is_colliding = False
        self.collision_detected = False
        self.clock = pygame.time.Clock()

        self.punching = False
        self.punching_retracting = False
        self.punching_angle = 0
        self.punching_speed = 15
        self.max_punching_angle = 90 

        self.walking = True
        self.right_leg_retracting = False
        self.right_leg_angle = 0

        self.left_leg_retracting = False
        self.left_leg_angle = 0

        self.max_leg_angle = 50

        self.leg_speed = self.speed / 2

        self.keys_pressed = {
            "left": False,
            "right": False,
            "up": False,
            "down": False,
            "ctrl": False
        }

        self.mouse_x = 0
        self.mouse_y = 0

        self.max_head_rotation = 15

        self.tile = Tile(self.screen, self.screen.get_width(), self.screen.get_height()) 
        self.walk_cycle_speed = 0.1

        self.idle_angle = 0
        self.idle_speed = 0.1  
        self.idle_direction = 1
        
    def updateGravity(self) -> None:
        """Update player's gravity."""
        dt = self.clock.tick(120) / 1000 
        if not self.isGrounded:
            self.velocity_y += (self.gravity * dt) * 3
            self.y_pos += self.velocity_y * dt
            self.player_rect.y = self.y_pos

    def getPlyrName(self) -> str:
        """Returns player name"""
        return self.name

    def handle_input(self):
        """Handle player input for movement."""
        keys = pygame.key.get_pressed()
        dx = (keys[K_RIGHT] - keys[K_LEFT]) * self.speed
        if dx != 0:
            self.walking = True
            if dx > 0: 
                self.facing_right = True
            else:
                self.facing_right = False
            self.move(dx)
        else:
            self.walking = False
        
        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()

    def move(self, dx):
        """Move the player horizontally and vertically."""
        self.velocity_x = dx
        self.x_pos += dx
        self.player_rect.x = self.x_pos

    def jump(self, jump_strength: float):
        """Make the player jump with the given jump strength."""
        self.velocity_y = -jump_strength

    def handleKeyPress(self, event):
        """Handle key press events."""
        if event.key == K_LEFT:
            self.keys_pressed["left"] = True
        elif event.key == K_RIGHT:
            self.keys_pressed["right"] = True
        elif event.key == K_UP:
            self.keys_pressed["up"] = True
        elif event.key == K_DOWN:
            self.keys_pressed["down"] = True
        elif event.key == K_LCTRL:
            self.keys_pressed["ctrl"] = True
            self.speed += 1

    def handleKeyRelease(self, event):
        """Handle key release events."""
        if event.key == K_LEFT:
            self.keys_pressed["left"] = False
        elif event.key == K_RIGHT:
            self.keys_pressed["right"] = False
        elif event.key == K_UP:
            self.keys_pressed["up"] = False
        elif event.key == K_DOWN:
            self.keys_pressed["down"] = False
        elif event.key == K_LCTRL:
            self.keys_pressed["ctrl"] = False
            self.speed -= 1
            
    def rotate(self, surf, image, pos, originPos, angle, right=True):
        """Legs rotation."""
        offsetx = 0
        offsety = 0
        if self.walking:
            ## To prevent the legs to be offset while player idling ##
            if self.facing_right:
                ## If player is facing right ##
                if right:
                    ## Right Leg ##
                    offsetx = 4 
                    offsety = 4
                else:
                    # Left Leg ##
                    offsetx = 7
                    offsety = 3
            else:
                ## If player facing left ##
                if right:
                    ## Right Leg ##
                    offsetx = 7
                    offsety = 6
                else:
                    ## Left Leg ##
                    offsetx = 6
                    offsety = 3

        image_rect = image.get_rect(topleft=(pos[0] - originPos[0] - offsetx, pos[1] - originPos[1] - offsety))
        offset_center_to_pivot = pygame.math.Vector2(pos) - image_rect.center
        rotated_offset = offset_center_to_pivot.rotate(-angle)
        rotated_image_center = (pos[0] - rotated_offset.x, pos[1] - rotated_offset.y)
        rotated_image = pygame.transform.rotate(image, angle)
        rotated_image_rect = rotated_image.get_rect(center=rotated_image_center)

        return rotated_image, rotated_image_rect

    def draw(self) -> None:
        """Draw the player on the screen."""

        ## Draw legs ##
        ########################################################################
        leg = pygame.transform.scale(self.right_leg, (4 * 3, 12 * 3))
        scaled_right_legs = pygame.transform.scale(self.right_leg, (4 * 3, 12 * 3))
        scaled_left_legs = pygame.transform.scale(self.left_leg, (4 * 3, 12 * 3))
        ########################################################################

        ########################################################################
        rotated_right_legs, right_leg_rect = self.rotate(self.screen, scaled_right_legs, (self.x_pos, self.y_pos + 36), (4 * 3 // 2, 12 * 3 // 2), self.right_leg_angle, True)
        rotated_left_legs, left_leg_rect = self.rotate(self.screen, scaled_left_legs, (self.x_pos, self.y_pos + 36), (4 * 3 // 2, 12 * 3 // 2), self.left_leg_angle, False)
        ########################################################################

        leg_rect = leg.get_rect(center=(self.x_pos, self.y_pos + 36))

        self.legs_rect = leg_rect

        if self.facing_right:
            self.screen.blit(rotated_right_legs, right_leg_rect)
            self.screen.blit(rotated_left_legs, left_leg_rect)
        else:
            self.screen.blit(pygame.transform.flip(rotated_left_legs, True, False), left_leg_rect)
            self.screen.blit(pygame.transform.flip(rotated_right_legs, True, False), right_leg_rect)

        ## Draw torso ##
        scaled_torso = pygame.transform.scale(self.torso, (4 * 3, 12 * 3))
        self.torso_rect = scaled_torso.get_rect()
        self.torso_rect.midbottom = right_leg_rect.midtop
        if self.facing_right:
            self.screen.blit(scaled_torso, self.torso_rect)
        else:
            flipped_torso = pygame.transform.flip(scaled_torso, True, False)
            self.torso_rect.midbottom = right_leg_rect.midtop
            self.torso_rect.left = right_leg_rect.left - (self.torso_rect.right - right_leg_rect.right)
            self.screen.blit(flipped_torso, self.torso_rect)

        ## Draw hand ##
        scaled_hand = pygame.transform.scale(self.hand, (4 * 3, 12 * 3))
        rotated_hand = pygame.transform.rotate(scaled_hand, self.punching_angle)
        hand_rect = rotated_hand.get_rect()
        hand_rect.centerx = self.torso_rect.centerx
        hand_rect.top = self.torso_rect.top
        if self.facing_right:
            if self.punching:
                hand_rect.centerx += 8
            self.screen.blit(rotated_hand, hand_rect)
        else:
            if self.punching:
                hand_rect.centerx -= 8
            self.screen.blit(pygame.transform.flip(rotated_hand, True, False), hand_rect)

        ## Draw head ##
        scaled_head = pygame.transform.scale(self.head, (8 * 3, 8 * 3))
        head_rect = scaled_head.get_rect()
        head_rect.midbottom = self.torso_rect.midtop

        angle_to_mouse = math.atan2(self.mouse_y - head_rect.centery, self.mouse_x - head_rect.centerx)
        angle_to_mouse_deg = math.degrees(angle_to_mouse)
        angle_to_mouse_deg = max(-self.max_head_rotation, min(angle_to_mouse_deg, self.max_head_rotation))

        if self.facing_right:
            if angle_to_mouse_deg < 0:
                head_rect.bottom -= 2
                head_rect.right -= 2
            else:
                head_rect.top += 2

            if angle_to_mouse_deg > 0:
                head_rect.right += 2
                head_rect.top -= 2
            else:
                head_rect.left += 2
                head_rect.top += 2

            self.screen.blit(pygame.transform.rotate(scaled_head, -angle_to_mouse_deg), head_rect)
        else:
            flipped_head = pygame.transform.flip(scaled_head, True, False)
            head_rect.midbottom = self.torso_rect.midtop

            if angle_to_mouse_deg < 0:
                head_rect.bottom -= 2
                head_rect.left -= 2
            else:
                head_rect.top += 1

            if angle_to_mouse_deg > 0:
                head_rect.left += 2
                head_rect.top -= 2
            else:
                head_rect.right += 2
                head_rect.top += 2

            head_rect.left = self.torso_rect.left - (head_rect.right - self.torso_rect.right)
            self.screen.blit(pygame.transform.rotate(flipped_head, angle_to_mouse_deg), head_rect)

    def punch(self):
        """Start the punching animation."""
        self.punching = True

    def update_punch(self):
        """Update the punching."""
        if self.punching:
            if not self.punching_retracting:
                self.punching_angle += self.punching_speed
                if self.punching_angle >= self.max_punching_angle:
                    self.punching_angle = self.max_punching_angle 
                    self.punching_retracting = True
            else:
                self.punching_angle -= self.punching_speed
                if self.punching_angle <= 0:
                    self.punching_angle = 0
                    self.punching_retracting = False 
                    self.punching = False 
        else:
            if self.velocity_x < 0:
                self.idle_angle += self.idle_speed * self.idle_direction
                if abs(self.idle_angle) >= 15:
                    self.idle_direction *= -1 
            else:
                self.idle_angle = 0

    def update_leg(self):
        """Update legs when walking"""
        if self.walking:
            if not self.right_leg_retracting:
                self.right_leg_angle += self.leg_speed
                if self.right_leg_angle >= self.max_leg_angle:
                    self.right_leg_angle = self.max_leg_angle
                    self.right_leg_retracting = True
            else:
                self.right_leg_angle -= self.leg_speed
                if self.right_leg_angle <= 0:
                    self.right_leg_angle = 0
                    self.right_leg_retracting = False

            if not self.left_leg_retracting:
                self.left_leg_angle -= self.leg_speed
                if self.left_leg_angle <= -self.max_leg_angle:
                    self.left_leg_angle = -self.max_leg_angle
                    self.left_leg_retracting = True
            else:
                self.left_leg_angle += self.leg_speed
                if self.left_leg_angle >= 0:
                    self.left_leg_angle = 0
                    self.left_leg_retracting = False
        else:
            self.right_leg_angle = 0
            self.left_leg_angle = 0
                      

    def checkCollision(self, rects) -> None:
        """
        Check collision between the player and tiles.
        """
        self.collision_detected = False
        self.isGrounded = False

        for (x, y), rect in rects.items():
            if self.legs_rect.colliderect(rect) or self.torso_rect.colliderect(rect):
                self.handleCollision(rect)
                self.collision_detected = True
                break

        if self.collision_detected and self.velocity_y >= 0:
            self.isGrounded = True
        else:
            self.isGrounded = False

    def handleCollision(self, rect) -> None:
        """
        Handle collision with a tile.
        """
        self.velocity_y = 0

    def is_position_far(self, x: float, y: float, distance_threshold: float) -> bool:
        """
        Check if the player's position is far from the given point based on the distance threshold.
        """
        distance_squared = (self.x_pos - x) ** 2 + (self.y_pos - y) ** 2
        return distance_squared > distance_threshold ** 2  

    
    def placeTile(self, tile_type: TileType, mouse_pos):
        self.punch()
        x_pos = (mouse_pos[0] // 32) * 32
        y_pos = (mouse_pos[1] // 32) * 32
        if (x_pos, y_pos) in (self.x_pos, self.y_pos):
            print("tt")
        else:
            if (x_pos, y_pos + 32) in TILES:
                self.tile.placeTile(tile_type, x_pos, y_pos)
            elif (x_pos, y_pos - 32) in TILES:
                self.tile.placeTile(tile_type, x_pos, y_pos)
            elif (x_pos + 32, y_pos) in TILES:
                self.tile.placeTile(tile_type, x_pos, y_pos)
            elif (x_pos - 32, y_pos) in TILES:
                self.tile.placeTile(tile_type, x_pos, y_pos)
    
    def destroyTile(self, mouse_pos):
        self.punch()
        x_pos = (mouse_pos[0] // 32) * 32
        y_pos = (mouse_pos[1] // 32) * 32
        self.tile.destroyTile(x_pos, y_pos)