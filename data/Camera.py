from data.settings import SIZE, F_SIZE


class Camera:
    x = y = 0
    width, height = 500, 300

    @staticmethod
    def render(target_x, target_y):
        if Camera.x + Camera.width > target_x:
            Camera.x = target_x - Camera.width
        if Camera.x + SIZE[0] - Camera.width < target_x:
            Camera.x = target_x - SIZE[0] + Camera.width

        if Camera.y + Camera.height > target_y:
            Camera.y = target_y - Camera.height
        if Camera.y + SIZE[1] - Camera.height < target_y:
            Camera.y = target_y - SIZE[1] + Camera.height

        if Camera.x < 0:
            Camera.x = 0
        elif Camera.x + SIZE[0] > F_SIZE[0]:
            Camera.x = F_SIZE[0] - SIZE[0]
        if Camera.y < 0:
            Camera.y = 0
        elif Camera.y + SIZE[1] > F_SIZE[1]:
            Camera.y = F_SIZE[1] - SIZE[1]

    @staticmethod
    def get_pos(x, y, rounded=False):
        if rounded:
            return round(x - Camera.x), round(y - Camera.y)
        else:
            return x - Camera.x, y - Camera.y