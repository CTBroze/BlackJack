from card import Card;
from deck import Deck;
import people;
import chip;
import sys;
import time;
import pygame;

#색 정의
BlACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
GRAY = (190,190,190)

#좌표 및 크기
size = [600, 400]
DEALER_X = 150
DEALER_Y = 0
PLAYER_X = 100
PLAYER_Y = 300

#전역변수
wait = True
seq = 0
dd = 0
player = people.Player("Player", 1000)
dealer = people.Dealer(Deck(6))

#게임 초기화
def startGame():
    global font, screen, clock, hitB, standB, doubleDownB

    #화면 설정
    pygame.init()
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('BlackJack')
    clock = pygame.time.Clock()
    
    #배경
    screen.fill((0,70,50))
    font = pygame.font.Font(None, 18)
    pygame.display.update()

    resetScreen()

def drawObject(obj,x,y):
    global screen
    screen.blit(obj,(x,y)) 

def resetScreen() :
    global font, screen, clock, hitB, standB, doubleDownB, resetB, DEALER_X, PLAYER_X

    DEALER_X = 150
    PLAYER_X = 100

    #딜러 섹션
    screen.fill((0,70,50))
    pygame.draw.line(screen, WHITE, (150, 0), (450, 0), 3)
    pygame.draw.line(screen, WHITE, (150, 0), (150, 100), 3)        
    pygame.draw.line(screen, WHITE, (150, 100), (450, 100), 3)
    pygame.draw.line(screen, WHITE, (450, 100), (450, 0), 3)

    #플레이어 섹션
    pygame.draw.line(screen, WHITE, (100, 300), (500, 300), 3)
    pygame.draw.line(screen, WHITE, (100, 300), (100, 400), 3)        
    pygame.draw.line(screen, WHITE, (100, 400), (500, 400), 3)
    pygame.draw.line(screen, WHITE, (500, 300), (500, 400), 3)

    #참가자 정보 출력 섹션
    pygame.draw.rect(screen, WHITE, [480, 150, 120, 100], 3)
    hitB = pygame.draw.rect(screen, GRAY,[483,153,50,30])
    standB = pygame.draw.rect(screen, GRAY,[547,153,50,30])
    doubleDownB = pygame.draw.rect(screen, GRAY,[483,193,50,30])
    resetB = pygame.draw.rect(screen, GRAY,[547,193,50,30])

    #입력 버튼 섹션
    pygame.draw.rect(screen, WHITE, [0, 150, 120, 100], 3)

    # Display some text
    text_dealer = font.render("Dealer", True, WHITE)
    text_player = font.render("Player", True, WHITE)
    text_player_info = font.render("Player Info", True, WHITE)
    text_name = font.render("Name :",True,WHITE)
    text_player_name = font.render(player.name,True,WHITE)
    text_hit = font.render("hit",True, BlACK)
    text_stand = font.render("stand",True,BlACK)
    text_doubleDown = font.render("DD",True,BlACK)
    text_reset = font.render("reset",True,BlACK)

    drawObject(text_hit,486,156)
    drawObject(text_stand,550,156)
    drawObject(text_doubleDown,486,196)
    drawObject(text_reset,550,196)
    drawObject(text_dealer, 150, 105)
    drawObject(text_player, 100, 285)
    drawObject(text_player_info, 30, 155)
    drawObject(text_name,5,170)
    drawObject(text_player_name,50,170)

    pygame.display.update()


def reset() :
    global player, dealer
    dealer.retrieve_cards(player)
    dealer.retrieve_cards(dealer)
    player.bet = 0

def view_hands() :
    global PLAYER_X
    drawObject(pygame.image.load("images/"+dealer.hand[0][0].img_url()).convert_alpha(), DEALER_X, DEALER_Y)
    drawObject(pygame.image.load("images/"+player.hand[0][0].img_url()).convert_alpha(), PLAYER_X, PLAYER_Y)
    PLAYER_X += 70;
    drawObject(pygame.image.load("images/"+player.hand[0][1].img_url()).convert_alpha(), PLAYER_X, PLAYER_Y)
    pygame.display.update()

def deal(dealer, players) :
    if not player.check_broke() : dealer.deal_card(player)
    dealer.deal_card(dealer)

def main():
    global seq, player, dealer, clock, PLAYER_X, DEALER_X, dd
    #이벤트 루프
    done = False
    while not done:
        if seq == 0:
            reset()
            player.bet = 100
            for i in range(0,2) :
                deal(dealer, player)
            view_hands()
            text_money = font.render("Money :"+str(player.money)+"$",True,WHITE)
            text_bet = font.render("Bet : "+str(player.bet)+"$",True,WHITE)
            drawObject(text_money,5,185)
            drawObject(text_bet,5,200)
            pygame.display.update()
            seq = 1
        for event in pygame.event.get():
            #종료버튼
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            #hit버튼 클릭
            elif event.type == pygame.MOUSEBUTTONDOWN and hitB.collidepoint(pygame.mouse.get_pos()):
                dealer.deal_card(player)
                PLAYER_X += 70
                drawObject(pygame.image.load("images/"+player.hand[0][-1].img_url()).convert_alpha(),PLAYER_X,PLAYER_Y)
                pygame.display.update()
                dd = 1
                if player.check_bust():
                    player.money -= player.bet
                    text_info = font.render("Lose, 5sec After Restart Game",True,WHITE)
                    drawObject(text_info,200,200)
                    pygame.display.update()
                    time.sleep(5)
                    resetScreen()
                    seq = 0
                    dd = 0
            #stand버튼 클릭
            elif event.type == pygame.MOUSEBUTTONDOWN and standB.collidepoint(pygame.mouse.get_pos()):
                DEALER_X += 70
                drawObject(pygame.image.load("images/"+dealer.hand[0][1].img_url()).convert_alpha(),DEALER_X,DEALER_Y)
                pygame.display.update()
                i = 2
                #딜러가 버스트 하거나 하드17이 될때까지 딜러의 카드 추가
                while not dealer.check_bust() and not dealer.check_hard_17() : 
                    dealer.deal_card(dealer)
                    DEALER_X += 70
                    drawObject(pygame.image.load("images/"+dealer.hand[0][i].img_url()).convert_alpha(),DEALER_X,DEALER_Y)
                    pygame.display.update()
                    i+=1
                #딜러가 버스트한경우
                if dealer.check_bust() :
                    #플레이어가 버스트하지 않은경우
                    if not player.check_bust():
                        if player.check_five_c():
                            text_info = font.render("Win(5-Charly), 5sec After Restart Game",True,WHITE)
                            drawObject(text_info,200,200)
                            pygame.display.update();
                            player.money += player.bet * 1.5
                        else:
                            text_info = font.render("Win, 5sec After Restart Game",True,WHITE)
                            drawObject(text_info,200,200)
                            pygame.display.update();
                            player.money += player.bet
                    #플레이어가 버스트한경우
                    else:
                        text_info = font.render("Lose, 5sec After Restart Game",True,WHITE)
                        drawObject(text_info,200,200)
                        pygame.display.update();
                        player.money -= player.bet
                #딜러가 버스트하지 않은경우
                else:
                    #플레이어가 버스트하지 않은경우
                    if not player.check_bust():
                        #5-찰리
                        if player.check_five_c():
                            text_info = font.render("Win(5-Charly), 5sec After Restart Game",True,WHITE)
                            drawObject(text_info,200,200)
                            pygame.display.update();
                            player.money += player.bet * 1.5
                        #플레이어가 이긴경우
                        elif player.hand_value() > dealer.hand_value():
                            text_info = font.render("Win, 5sec After Restart Game",True,WHITE)
                            drawObject(text_info,200,200)
                            pygame.display.update();
                            player.money += player.bet
                        #플레이어가 진경우
                        elif player.hand_value() < dealer.hand_value():
                            text_info = font.render("Lose, 5sec After Restart Game",True,WHITE)
                            drawObject(text_info,200,200)
                            pygame.display.update();
                            player.money -= player.bet
                        #플레이어가 비긴경우
                        else :
                            text_info = font.render("Draw, 5sec After Restart Game",True,WHITE)
                            drawObject(text_info,200,200)
                            pygame.display.update();
                    #플레이어가 버스트한경우
                    else:
                        text_info = font.render("Lose, 5sec After Restart Game",True,WHITE)
                        drawObject(text_info,200,200)
                        pygame.display.update();
                        player.money -= player.bet
                time.sleep(5)
                resetScreen()
                seq = 0
                dd = 0
            #doubleDown버튼 클릭
            elif event.type == pygame.MOUSEBUTTONDOWN and doubleDownB.collidepoint(pygame.mouse.get_pos()):
                if dd == 0:
                    player.bet += player.bet
                    text_bet = font.render("Bet : "+str(player.bet)+"$",True,WHITE)
                    pygame.draw.rect(screen,(0,70,50),[5,200,60,14])
                    drawObject(text_bet,5,200)
                    pygame.display.update()
                    dd = 1
            #reset버튼 클릭
            elif event.type == pygame.MOUSEBUTTONDOWN and resetB.collidepoint(pygame.mouse.get_pos()):
                player = people.Player(player.name,1000)
                dealer = people.Dealer(Deck(6))
                text_info = font.render("Reset Game, 5sec After Restart Game",True,WHITE)
                drawObject(text_info,200,200)
                pygame.display.update()
                time.sleep(5)
                resetScreen()
                seq = 0
                dd = 0


    #화면 그리기
    clock.tick(60)

startGame()
main()

