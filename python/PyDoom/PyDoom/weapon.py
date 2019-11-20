

class DefaultWeapon:
    def __init__(self):
        self.name = "Default"
        self.sprite = "hot-dog.png"
        self.fire_sound = "bang.wav"

        self.clip_size = 10

        self.rate_of_fire = 1

        self.__ammo = 0

    @property
    def ammo(self):
        return self.__ammo

    @ammo.setter
    def ammo(self, val):
        self.__ammo -= val

    def shoot(self, entity):
        """
        :param entity: Source entity
        :return:
        """
        if self.ammo > 0:
            self.ammo -= 1
            # Spawn projectile
            # Create fire sound
        else:
            # Reload?
            # Gun click sound?
            pass

