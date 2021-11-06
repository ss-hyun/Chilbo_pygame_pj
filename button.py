import pygame

class Button:
    def __init__(self, up_img, down_img, pos, action, *args):
        self.up_img = up_img
        self.down_img = down_img
        self.size = up_img.get_rect().size
        self.pos = pos
        self.xstart = pos[0]
        self.xend = pos[0] + self.size[0]
        self.ystart = pos[1]
        self.yend = pos[1] + self.size[1]
        self.action = action
        self.args = args
    
    def draw(self, background):
        m_xpos, m_ypos = pygame.mouse.get_pos()
        if m_xpos > self.xstart and m_xpos < self.xend and m_ypos > self.ystart and m_ypos < self.yend:
            background.blit(self.down_img, self.pos)
        else:
            background.blit(self.up_img, self.pos)

    def click(self):
        m_xpos, m_ypos = pygame.mouse.get_pos()
        if m_xpos > self.xstart and m_xpos < self.xend and m_ypos > self.ystart and m_ypos < self.yend:
            if self.action != None:
                self.action(*self.args)