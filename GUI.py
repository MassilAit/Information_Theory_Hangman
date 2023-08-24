import pygame
import sys
import solver

WIN_SIZE=(800,500)


class Button:
    def __init__(self):
        self.image=pygame.image.load('graphics/button.png',).convert_alpha()
        self.rec=self.image.get_rect(bottomright=(780,480))

    def draw(self,win):
        win.blit(self.image,self.rec)

    def is_clicked(self,pos):
        return self.rec.collidepoint(pos)


class Letter:
    def __init__(self,character:chr, position:tuple,font):
        self.font=font
        self.position=position
        self.image=self.font.render(character,False,'black')
        self.rec=self.image.get_rect(topleft=position)

    def is_selected(self,position):
        return self.rec.collidepoint(position)


class Word:
    OFFSET=25

    def __init__(self, len : int):
        self.n=len
        self.font = pygame.font.Font(None, 50)
        self.l=[]
        self.current_state=[0]*len
        self.modified=[]
        self.locked=set()
        x=230
        for i in range(len):
            self.l.append(Letter('_',(x,330),self.font))
            x+=35

    def update_locked(self):
        x=len(self.locked)
        for i, l in enumerate(self.current_state):
            if l != 0:
                self.locked.add(i)
        return x==len(self.locked)

    def is_selected(self,position, win):
        for i in range(self.n):
            if self.l[i].is_selected(position) and i not in self.locked:
                self.select(i,win)
                return True

    def select(self,index,win):
        self.l[index].image=self.font.render('_',False,'red')
        letters=['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n',
                 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.l[index].image = self.font.render('_', False, 'black')
                    return
                if event.type == pygame.KEYDOWN:
                    if event.unicode in letters:
                        self.change_letter(event.unicode, index)
                    if event.key==pygame.K_RETURN:
                        self.l[index].image = self.font.render('_', False, 'black')

                        return

            pygame.draw.rect(win, 'white', self.l[index].rec)
            self.draw(win)
            pygame.display.flip()

    def draw(self,win):
        for c in self.l:
            win.blit(c.image, c.rec)

    def change_letter(self,letter, index):
        self.current_state[index]=letter
        for t in self.modified:
            if t[0]==index:
                self.l[t[1]]=Letter(letter, self.l[index].position, self.font)
                return
        self.l.append(Letter(letter, self.l[index].position, self.font))
        self.modified.append((index, len(self.l)-1))

    def delete_letter(self,index):
        self.change_letter('',index)
        self.current_state[index] = 0


def update_gallow(failed_guess : int) :
    return pygame.image.load('graphics/hang'+str(failed_guess)+'.png').convert_alpha()


def start_game(win):
    font = pygame.font.Font(None, 40)
    q = font.render('Please enter the number of letters in your word : ', False, 'black')
    q_rec = q.get_rect(topleft=(10,225))
    input=""
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type==pygame.KEYDOWN:
                if event.unicode in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] and len(input)<2:
                    input+=event.unicode
                if event.key==pygame.K_BACKSPACE:
                    if len(input)>0:
                        input=input[:-1]
                if event.key==pygame.K_RETURN:
                    if len(input)>0:
                        run=False



        a=font.render(input,False, 'black')
        a_rec=a.get_rect(topleft=(q_rec.right+10,225))

        win.fill('white')

        win.blit(q,q_rec)
        win.blit(a, a_rec)
        pygame.display.flip()

    win.fill('white')
    pygame.display.flip()
    return int(input)


def draw_computer_guess(c : chr, win):
    font=pygame.font.Font(None, 35)
    a = font.render('The computer guessed  : ', False, 'black')
    b=font.render(c.upper(), False, 'black')
    a_rec = a.get_rect(bottomright=(600, 100))
    b_rec = b.get_rect(midtop=a_rec.midbottom)
    win.blit(a, a_rec)
    win.blit(b,b_rec)


def draw_winning(win, s):
    font = pygame.font.Font(None, 50)
    a = font.render('Your word is : ', False, 'black')
    b = font.render(s, False, 'black')
    a_rec = a.get_rect(midtop=(400, 150))
    b_rec = b.get_rect(midtop=a_rec.midbottom)
    win.fill('white')
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type==pygame.KEYDOWN:
                pygame.quit()
                sys.exit()
        win.blit(a, a_rec)
        win.blit(b, b_rec)
        pygame.display.update()


def draw_corresponding_words(win, words: int):
    font = pygame.font.Font(None, 25)
    a = font.render('Corresponding words : ', False, 'black')
    b = font.render(str(words), False, 'black')
    a_rec = a.get_rect(bottomleft=(10,460))
    b_rec = b.get_rect(midtop=a_rec.midbottom)
    win.blit(a, a_rec)
    win.blit(b, b_rec)


def draw_losing(win):
    font = pygame.font.Font(None, 50)
    a = font.render("The computer couldn't guess your  ", False, 'black')
    b = font.render("word in less then 10 guesses", False, 'black')
    a_rec = a.get_rect(midtop=(400, 150))
    b_rec = b.get_rect(midtop=a_rec.midbottom)
    win.fill('white')
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type==pygame.KEYDOWN:
                pygame.quit()
                sys.exit()
        win.blit(a, a_rec)
        win.blit(b, b_rec)
        pygame.display.update()

def word_not_found(win):
    font = pygame.font.Font(None, 50)
    a = font.render("Your word is not in ", False, 'black')
    b = font.render("our database", False, 'black')
    a_rec = a.get_rect(midtop=(400, 150))
    b_rec = b.get_rect(midtop=a_rec.midbottom)
    win.fill('white')
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                pygame.quit()
                sys.exit()
        win.blit(a, a_rec)
        win.blit(b, b_rec)
        pygame.display.update()


def main(file_name: str):
    pygame.init()
    win=pygame.display.set_mode(WIN_SIZE)
    win.fill('white')
    pygame.display.flip()
    pygame.display.set_caption("Hangman")

    n=start_game(win)

    run = True
    failed_guess=0

    gallow_surf = update_gallow(failed_guess)
    button=Button()
    word=Word(n)

    data=solver.get_data(file_name)
    if n not in data:
        word_not_found(win)
    words=data[n]
    guesses = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z']
    next_guess=True
    combs=[]
    dic={}
    old_state=[]
    guess=""

    while run :
        if next_guess:
            old_state=word.current_state.copy()
            x=solver.best_guess(guesses, words, old_state)
            combs=x[1]
            dic=x[2]
            guess=x[0]
            next_guess=False

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False

            if event.type==pygame.MOUSEBUTTONDOWN:
                pos=pygame.mouse.get_pos()
                word.is_selected(pos,win)


                if button.is_clicked(pos):
                    if word.update_locked():



                        failed_guess+=1
                    index=solver.find_index(solver.find_comb(old_state,word.current_state),combs)
                    if index not in dic:
                        word_not_found(win)
                    words=dic[index]
                    next_guess=True

        win.fill('white')
        win.blit(gallow_surf, (100, 100))
        draw_computer_guess(guess, win)
        draw_corresponding_words(win,len(words))
        word.draw(win)
        button.draw(win)
        gallow_surf = update_gallow(failed_guess)

        pygame.display.update()

        if len(words) == 1:
            draw_winning(win,words[0])
            run=False

        if failed_guess==10 :
            draw_losing(win)
            run=False


    pygame.quit()


main('data/words.json')