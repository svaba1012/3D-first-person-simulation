import pygame as pg
import math, time

STARTNIUGAO = 0
PI = math.pi
ALFA = PI * 2 / 3
BETA = PI * 2 / 3
WALL_DEPTH = 0.2
PLAYER_RADIUS = 0.2
displaySurface = pg.display.set_mode((0, 0), pg.FULLSCREEN)          
WIDTH, HEIGHT = displaySurface.get_size()
PLAYER_HEIGHT = 1.8
WALL_HEIGHT = 2.5
SENSITIVITY = 1 / 100
RADIUS = 5
COEF = 20
MALI_UGAO = 0
MINI_MAP_WIDTH = 300
MINI_MAP_HEIGHT = 300
VIDOKRUG = 1
pg.mouse.set_visible(False)

def miniMap(tReal):
    return [WIDTH // 2 + tReal[0] * COEF, HEIGHT // 2 + tReal[1] * COEF]

def staviUMiniMapu(centar, player, tacka):
    return [centar[0] + (tacka[0] - player[0]) * COEF, centar[1] + (tacka[1] - player[1]) * COEF]

def distance(t, player):
    return math.sqrt((t[0] - player[0]) ** 2 + (t[1] - player[1]) ** 2)

def angle(t, player):
    return (math.atan2(t[1] - player[1], t[0] - player[0])) % (2 * PI)
            
def angleDif(t, player, ugao):
    fi = angle(t, player)
    return (fi - ugao) % (2 * PI)

def isRight(teta1, teta2):
    if teta1 > PI:
        dg = teta1 - PI
        if teta2 < teta1 and teta2 > dg:
            return True
    else:
        dg = teta1 + PI
        if teta2 < teta1 or teta2 > dg:
            return True
    return False

def cosak(r, fi):
    d = abs(math.cos(fi1)) * r
    x = WIDTH / 2 * (1 + math.tan(fi) / math.tan(BETA / 2))
    y1 = (1 - ((WALL_HEIGHT - PLAYER_HEIGHT) / (math.tan(ALFA / 2) * d))) * HEIGHT / 2
    y2 = (1 + ((PLAYER_HEIGHT) / (math.tan(ALFA / 2) * d))) * HEIGHT / 2


def uVidokrugu(fi):
    rez = 10
    if fi < BETA / 2 or fi > 2 * PI - BETA / 2:
        rez = 0
    '''
    if fi > BETA / 2 and fi < BETA:
        rez = -1
    if fi < 2 * PI - BETA / 2 and fi > 2 * PI - BETA:
        rez = 1
    '''
    return rez

def zidIspred(fi1, fi2):
    if uVidokrugu(fi1) == 0 or uVidokrugu(fi2) == 0:
        return False
    '''
    if fi1 > PI:
        fi1 = 2 * PI - fi1
    if fi2 > PI:
        fi2 = 2 * PI - fi2
    '''
    return abs(fi2 - fi1) > PI

def presek(t1, t2, pPoz, ugao):
    ugao = ugao % (2 * PI)
    deltaX = t1[0] - t2[0]
    if deltaX != 0:
        k1 = (t1[1] - t2[1]) / deltaX
        n1 = t1[1] - k1 * t1[0]
    else:
        newX = t1[0]
    k2 = math.tan(ugao)
    fi = [angle(t1, pPoz), angle(t2, pPoz)]
    fi.sort()
    n2 = pPoz[1] - k2 * pPoz[0]
    if deltaX != 0:
        newX = (n2 - n1) / (k1 - k2)
    newY = k2 * newX + n2
    sinUgla = math.sin(ugao)
    znakSinUgla = sinUgla / abs(sinUgla)
    cosUgla = math.cos(ugao)
    znakCosUgla = cosUgla / abs(cosUgla)
    sinTacke = newY / distance([newX, newY], pPoz)
    cosTacke = newX / distance([newX, newY], pPoz)
    znakCosTacke = cosTacke / abs(cosTacke)
    znakSinTacke = sinTacke / abs(sinTacke)
    sortedY = [t1[1], t2[1]]
    sortedY.sort()
    sortedX = [t1[0], t2[0]]
    sortedX.sort()
    praviPresek = znakCosTacke == znakCosUgla and znakSinTacke == znakSinUgla
    prav = math.sin(ugao) * newY > 0 and math.cos(ugao) * newX > 0
    if newX >= sortedX[0] and newY >= sortedY[0] and  newX <= sortedX[1] and newY <= sortedY[1] and praviPresek:
        return [[newX, newY], praviPresek]
    else:
        return [t1, praviPresek]

def miniMapa(a, b, playerPoz, tacke, brojTacaka, spojevi, ugao1, ugao2):
    pozX = WIDTH - a
    pozY = HEIGHT - b
    pg.draw.rect(displaySurface, (0,0,0), (pozX, pozY, a, b))
    pg.draw.rect(displaySurface, (255,255,255), (pozX, pozY, a, b), 5)
    center = [pozX + a // 2, pozY + b // 2]
    pozPlayer = staviUMiniMapu(center, playerPoz, playerPoz)
    pozPlayer[0] = int(pozPlayer[0])
    pozPlayer[1] = int(pozPlayer[1])
    secDot = (math.cos(ugao1) * VIDOKRUG * COEF + pozPlayer[0], math.sin(ugao1) * VIDOKRUG * COEF + pozPlayer[1])
    thirdDot = (math.cos(ugao2) * VIDOKRUG * COEF + pozPlayer[0], math.sin(ugao2) * VIDOKRUG * COEF + pozPlayer[1])
    pg.draw.circle(displaySurface, (255, 255, 255), pozPlayer, RADIUS)
    pg.draw.arc(displaySurface, (255, 255, 255), (pozPlayer[0] - VIDOKRUG * COEF , pozPlayer[1] - VIDOKRUG * COEF , 2 * VIDOKRUG * COEF , 2 * VIDOKRUG * COEF ), -ugao1, -ugao2)
    pg.draw.line(displaySurface, (255, 255, 255), pozPlayer, secDot)
    pg.draw.line(displaySurface, (255, 255, 255), pozPlayer, thirdDot)
    for i in range(brojTacaka):
        for j in range(len(spojevi[i])):
            k = spojevi[i][j]
            if k < i:
                continue
            tackaNaMiniMapi1 = staviUMiniMapu(center, playerPoz, tacke[i])
            tackaNaMiniMapi2 = staviUMiniMapu(center, playerPoz, tacke[k])
            if (tackaNaMiniMapi1[0] < pozX or tackaNaMiniMapi1[1] < pozY) and (tackaNaMiniMapi2[0] < pozX or tackaNaMiniMapi2[1] < pozY):
                continue
            if tackaNaMiniMapi1[0] - tackaNaMiniMapi2[0] != 0:
                k = (tackaNaMiniMapi1[1] - tackaNaMiniMapi2[1]) / (tackaNaMiniMapi1[0] - tackaNaMiniMapi2[0])
                n = tackaNaMiniMapi1[1] - k * tackaNaMiniMapi1[0]
                y1 = k * pozX + n
                if k != 0:
                    x1 = (pozY - n) / k
                else:
                    x1 = pozX
            else:
                x1 = tackaNaMiniMapi1[0]
                y1 = pozY    
            if tackaNaMiniMapi1[0] < pozX and y1 >= pozY:
                tackaNaMiniMapi1 = [pozX, y1]
            elif tackaNaMiniMapi2[0] < pozX and y1 >= pozY:
                tackaNaMiniMapi2 = [pozX, y1]
            elif tackaNaMiniMapi1[1] < pozY and x1 >= pozX:
                tackaNaMiniMapi1 = [x1, pozY]
            elif tackaNaMiniMapi2[1] < pozY and x1 >= pozX:
                tackaNaMiniMapi2 = [x1, pozY]
            pg.draw.line(displaySurface, (255, 255, 255), tackaNaMiniMapi1, tackaNaMiniMapi2)

def kretanje(playerPoz, ugao, keys):
    gore = False
    dole = False
    kreceSe = False
    brzina = 0.001
    ugao1 = ugao
    if keys[8]:
        brzina *= 1.5
    if keys[0] or keys[4]:
        kreceSe = True
        gore = True
    if keys[2] or keys[6]:
        kreceSe = True
        dole = True
        ugao1 -= PI
    if keys[1] or keys[5]:
        kreceSe = True
        if gore:
            ugao1 -= (PI / 4)
        elif dole:
            ugao1 -= (3 * PI / 4)
        else:
            ugao1 -= (PI / 2)
    if keys[3] or keys[7]:
        kreceSe = True
        if gore:
            ugao1 += (PI / 4)
        elif dole:
            ugao1 += (3 * PI / 4)
        else:
            ugao1 += (PI / 2)
    if kreceSe:
        playerPoz[0] = playerPoz[0] + math.cos(ugao1) * brzina
        playerPoz[1] = playerPoz[1] + math.sin(ugao1) * brzina
    return playerPoz

tRealS = []
t = []
tRealS.append([-5, -5])
tRealS.append([2, 4])
tRealS.append([-2, 2])
tRealS.append([3, -5])
tRealS.append([-3, -5])
tRealS.append([0, -5])
veze = [[2, 4], [2, 3], [0, 1], [0, 5], [0], [3]]
brojTacaka = 4

for i in range(brojTacaka):
    t.append(miniMap(tRealS[i]))

realPozPlayer = [1, 1]
pozPlayer = miniMap(realPozPlayer)

ugao1 = STARTNIUGAO + BETA / 2
ugao2 = STARTNIUGAO - BETA / 2
r = 100
keys = [False, False, False, False, False, False, False, False, False]


while True:
    displaySurface.fill((0,200,0))
    mouseMovX, mouseMovY = pg.mouse.get_rel()
    ugao1 += mouseMovX * SENSITIVITY
    ugao2 += mouseMovX * SENSITIVITY
    ugao = ugao1 - BETA / 2
    realPozPlayer = kretanje(realPozPlayer, ugao, keys)
    pozPlayer = miniMap(realPozPlayer)
    for i in range(brojTacaka):
        for j in range(len(veze[i])):
            k = veze[i][j]
            if k < i:
                continue
            fiS1 = angleDif(tRealS[i], realPozPlayer, ugao)
            fiS2 = angleDif(tRealS[k], realPozPlayer, ugao)
            teta1 = angle(tRealS[i], realPozPlayer)
            teta2 = angle(tRealS[k], realPozPlayer)
            ugaoRazlike2 = ugao2 - MALI_UGAO
            ugaoRazlike1 = ugao1 + MALI_UGAO
            if isRight(teta1, teta2):
                ugaoRazlike1, ugaoRazlike2 = ugaoRazlike2, ugaoRazlike1
            tReal1, pravaStranaPreseka1 = presek(tRealS[i], tRealS[k], realPozPlayer, ugaoRazlike2)
            tReal2, pravaStranaPreseka2 = presek(tRealS[k], tRealS[i], realPozPlayer, ugaoRazlike1)
            r1 = distance(tReal1, realPozPlayer)
            r2 = distance(tReal2, realPozPlayer)
            fi1 = angleDif(tReal1, realPozPlayer, ugao)
            fi2 = angleDif(tReal2, realPozPlayer, ugao)

            d1 = abs(math.cos(fi1)) * r1
            x1 = WIDTH / 2 * (1 + math.tan(fi1) / math.tan(BETA / 2))
            y11 = (1 - ((WALL_HEIGHT - PLAYER_HEIGHT) / (math.tan(ALFA / 2) * d1))) * HEIGHT / 2
            y12 = (1 + ((PLAYER_HEIGHT) / (math.tan(ALFA / 2) * d1))) * HEIGHT / 2

            d2 = abs(math.cos(fi2)) * r2
            x2 = WIDTH / 2 * (1 + math.tan(fi2) / math.tan(BETA / 2))
            y21 = (1 - ((WALL_HEIGHT - PLAYER_HEIGHT) / (math.tan(ALFA / 2) * d2))) * HEIGHT / 2
            y22 = (1 + ((PLAYER_HEIGHT) / (math.tan(ALFA / 2) * d2))) * HEIGHT / 2

            #pg.draw.line(displaySurface, (255, 255, 255), t[i], t[k])
            if (uVidokrugu(fiS1) * uVidokrugu(fiS2) == 0 and (pravaStranaPreseka1 or pravaStranaPreseka2)) or zidIspred(fiS1, fiS2):
                pg.draw.polygon(displaySurface, (255,0,0), ((x1, y11), (x1, y12), (x2, y22), (x2, y21)))
                pg.draw.polygon(displaySurface, (0,0,0), ((x1, y11), (x1, y12), (x2, y22), (x2, y21)), 2)
            
    #secDot = (math.cos(ugao1) * r + pozPlayer[0], math.sin(ugao1) * r + pozPlayer[1])
    #thirdDot = (math.cos(ugao2) * r + pozPlayer[0], math.sin(ugao2) * r + pozPlayer[1])
    mouseX, mouseY = pg.mouse.get_pos()
    if mouseX > WIDTH - 10 or mouseY > HEIGHT - 10 or mouseX < 10 or mouseY < 10:
        pg.mouse.set_pos((WIDTH / 2, HEIGHT / 2))
        
    miniMapa(MINI_MAP_WIDTH, MINI_MAP_HEIGHT, realPozPlayer, tRealS, brojTacaka, veze, ugao1, ugao2)
    
    #pg.draw.line(displaySurface, (255, 255, 255), pozPlayer, secDot)
    #pg.draw.line(displaySurface, (255, 255, 255), pozPlayer, thirdDot)
    #pg.draw.circle(displaySurface, (255, 255, 255), pozPlayer, RADIUS)
    #pg.draw.arc(displaySurface, (255, 255, 255), (pozPlayer[0] - r, pozPlayer[1] - r, 2 * r, 2 * r), -ugao1, -ugao2)
    
    for event in pg.event.get() : 
        if event.type == pg.QUIT : 
            pg.quit() 
            quit()
        if event.type == pg.KEYDOWN:
            if event.key==pg.K_UP:
                keys[0]=True
            elif event.key==pg.K_LEFT:
                keys[1]=True
            elif event.key==pg.K_DOWN:
                keys[2]=True
            elif event.key==pg.K_RIGHT:
                keys[3]=True
            elif event.key==pg.K_w:
                keys[4] = True
            elif event.key==pg.K_a:
                keys[5] = True
            elif event.key==pg.K_s:
                keys[6] = True
            elif event.key==pg.K_d:
                keys[7] = True
            elif event.key==pg.K_LSHIFT:
                keys[8] = True

        if event.type == pg.KEYUP:
            if event.key==pg.K_UP:
                keys[0]=False
            elif event.key==pg.K_LEFT:
                keys[1]=False
            elif event.key==pg.K_DOWN:
                keys[2]=False
            elif event.key==pg.K_RIGHT:
                keys[3]=False
            elif event.key==pg.K_w:
                keys[4] = False
            elif event.key==pg.K_a:
                keys[5] = False
            elif event.key==pg.K_s:
                keys[6] = False
            elif event.key==pg.K_d:
                keys[7] = False
            elif event.key==pg.K_LSHIFT:
                keys[8] = False
        pg.display.update()
        pg.time.delay(50) 
    
