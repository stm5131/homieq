import pygame


def drawText(surface, text, color, rect, font, aa=False, bkg=None):
    rect = pygame.Rect(rect)
    y = rect.top
    lineSpacing = 0

    # get the height of the font
    fontHeight = font.size("Tg")[1]

    while text:
        i = 1

        # determine if the row of text will be outside our area
        if y + fontHeight > rect.bottom:
            break

        # determine maximum width of line
        while font.size(text[:i])[0] < rect.width and i < len(text):
            i += 1

        # if we've wrapped the text, then adjust the wrap to the last word      
        if i < len(text): 
            i = text.rfind(" ", 0, i) + 1

        # render the line and blit it to the surface
        if bkg:
            image = font.render(text[:i], 1, color, bkg)
            image.set_colorkey(bkg)
        else:
            image = font.render(text[:i], aa, color)

        surface.blit(image, (rect.left, y))
        y += fontHeight + lineSpacing

        # remove the text we just blitted
        text = text[i:]

    return text

class Text_box:
    def __init__(self,screen):
        #Box location, size, state flags and font
        self.location = ()
        self.size = ()
        self.start = False
        self.closing = False
        self.waiting = False
        self.newtext = False
        self.done = False
        self.font = pygame.font.Font('font/Pixeltype.ttf',45)
        self.screen = screen
        self.i = 0

    def draw_box(self,text,location,size,dt):
        if not self.start:
            if not self.closing:
                if not self.waiting:
                    self.start = True
                    self.i=0
                    self.done = False
        if self.start:
            if self.i < 1:
                self.i+=0.03*dt
            else:
                self.start = False
                self.waiting = True
                self.i=0
            box = pygame.Surface((10+size[0]*(self.i),10+size[1]))
            box.fill((0,0,0))
            self.screen.blit(box,location)
            box = pygame.Surface((size[0]*(self.i),size[1]))
            box.fill((25,25,25))

            self.screen.blit(box,(location[0]+5,location[1]+5))

        elif self.closing:
            if self.i < 1:
                self.i+=0.03*dt
            else:
                self.closing = False
                self.i=0
            box = pygame.Surface((10+size[0]*(self.i),10+size[1]))
            box.fill((0,0,0))
            self.screen.blit(box,location)
            box = pygame.Surface((size[0]*(self.i),size[1]))
            box.fill((25,25,25))

            self.screen.blit(box,(location[0]+5,location[1]+5))

        elif self.waiting:

            box = pygame.Surface((10+size[0],10+size[1]))
            box.fill((0,0,0))
            self.screen.blit(box,location)

            box = pygame.Surface((size[0],size[1]))
            box.fill((25,25,25))
            drawText(box,text[0:round(self.i)],(255,255,255),box.get_rect(),self.font)
            self.screen.blit(box,(location[0]+5,location[1]+5))

            if round(self.i)<len(text):
                self.i+=0.35*dt
            else:
                self.done = True
            if self.newtext:
                self.newtext=False
                self.i=0
class Button:
    def __init__(self,screen,size):
        #Box location, size, state flags and font
        self.location = ()
        self.size = ()
        self.font = pygame.font.Font('font/Pixeltype.ttf',30)
        self.box = pygame.Surface(size)
        self.box_rect = self.box.get_rect()
        self.size = size
        self.screen = screen
    def draw_box(self,location,text):
        if self.is_clicked():
            self.box.fill((100,100,100))
        else:
            self.box.fill((0,0,0))

        self.box.set_alpha(200)

        button_text = self.font.render(text, False, (255,255,255))
        self.box_rect = self.box.get_rect()
        text_rect = button_text.get_rect(center = self.box_rect.center)

        self.box.blit(button_text, text_rect)
        self.screen.blit(self.box,location)

        self.box_rect = self.box.get_rect(topleft = location)

    def is_clicked(self):
        return pygame.mouse.get_pressed()[0] and self.box_rect.collidepoint(pygame.mouse.get_pos())

