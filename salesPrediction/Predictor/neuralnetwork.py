from math import exp

def predict(inputVectorCount=12, learnAndTestCount=11, salesData={}):
    lr = 2  # learning rate

    patternFromFirstProduct = [None] * learnAndTestCount
    index = 0
    for month in salesData:
        #print(index)
        if index >= learnAndTestCount:
            break
        for product in salesData[month]:
            patternFromFirstProduct[index] = salesData[month][product]
            index += 1
            break

    #print(patternFromFirstProduct)
    #print(len(patternFromFirstProduct))

    for i in range(learnAndTestCount):
        patternFromFirstProduct[i] = patternFromFirstProduct[i] / max(patternFromFirstProduct)

    print(patternFromFirstProduct)
    # do ogarniecia wzorzec
    #d = [45.64 / 46.76, 45.92 / 46.76, 46.32 / 46.76, 46.76 / 46.76]  # wzorzec
    d = patternFromFirstProduct
    n = 100  # liczba epok

    w111 = [None] * 101
    w112 = [None] * 101
    w121 = [None] * 101
    w122 = [None] * 101

    w21 = [None] * 101
    w22 = [None] * 101

    beta = [None] * 100
    beta21 = [None] * 100
    beta22 = [None] * 100
    bb = [None] * 100
    yy21 = [None] * 100

    w1s2 = [None] * 101  # wektor dla wag skrosnych, wejscie 1 z jednostka 2
    w2s2 = [None] * 101  # wektor dla wag skrosnych, wejscie 2 z jednostka 2
    w3s1 = [None] * 101  # wektor dla wag skrosnych, wejscie 3 z jednostka 1
    w4s1 = [None] * 101  # wektor dla wag skrosnych, wejscie 4 z jednostka 1

    dw111 = [None] * 100  # wartosc o jaka zmieni sie waga w111 w danym kroku obliczeniowym,
    dw112 = [None] * 100  # wartosc o jaka zmieni sie waga w112 w danym kroku obliczeniowym,
    dw121 = [None] * 100  # wartosc o jaka zmieni sie waga w121 w danym kroku obliczeniowym,
    dw122 = [None] * 100  # poniewaz chcemy wyliczyc jak zmieniaja sie wszystkie wagi

    dw1s2 = [None] * 100  # jest to wektor do zmiennej wagi ktore laczy wejscie 1 z jednostka druga
    dw2s2 = [None] * 100  # jest to wektor do zmiennej wagi ktore laczy wejscie 2 z jednostka druga
    dw3s1 = [None] * 100  # jest to wektor do zmiennej wagi ktore laczy wejscie 3 z jednostka pierw.
    dw4s1 = [None] * 100  # jest to wektor do zmiennej wagi ktore laczy wejscie 4 z jednostka pierw.

    dw21 = [None] * 100  # wektor dla zmiany wagi w21
    dw22 = [None] * 100  # wektor dla zmiany wagi w22

    blad = [None] * 100  # blad sredniokwadratowy
    # blad= suma ((d-u)*(d-u))

    u1 = [None] * learnAndTestCount  # wektor wejsc spolki gieldowej PKOBP
    u2 = [None] * learnAndTestCount  # wektor wejsc spolki gieldowej ALIOR
    u3 = [None] * learnAndTestCount  # wektor wejsc spolki gieldowej Tauron PE
    u4 = [None] * learnAndTestCount  # wektor wejsc spolki gieldowej Oragne PL

    index = 0
    for month in salesData:
        u1[index], u2[index], u3[index], u4[index] = salesData[month].values()
        index += 1
        if index >= learnAndTestCount:
            break

    u1Max = max(u1)
    u2Max = max(u2)
    u3Max = max(u3)
    u4Max = max(u4)

    for i in range(learnAndTestCount):
        u1[i] = u1[i] / u1Max
        u2[i] = u2[i] / u2Max
        u3[i] = u3[i] / u3Max
        u4[i] = u4[i] / u4Max

    print("Dane uczenia: ", u1, u2, u3, u4)

    '''
    u1[0] = 45.64 / 46.76  # sygnaly wejsc Asseco
    u1[1] = 45.92 / 46.76
    u1[2] = 46.32 / 46.76
    u1[3] = 46.76 / 46.76

    u2[0] = 43.27 / 43.27  # sygnaly wejsc PKO BP
    u2[1] = 42.59 / 43.27
    u2[2] = 42.88 / 43.27
    u2[3] = 40.65 / 43.27

    u3[0] = 149.50 / 150  # sygnaly wejsc Comarch
    u3[1] = 150 / 150
    u3[2] = 147 / 150
    u3[3] = 145 / 150

    u4[0] = 106 / 109.8  # sygnaly wejsc CD Projekt
    u4[1] = 103.6 / 109.8
    u4[2] = 109.8 / 109.8
    u4[3] = 108.2 / 109.8
    '''
    # poczatkowe wartosci wag

    w111[0] = -0.8
    w112[0] = 0.77
    w121[0] = 0.82
    w122[0] = -0.86

    w1s2[0] = -0.9
    w2s2[0] = 0.3
    w3s1[0] = 0.5
    w4s1[0] = -0.7

    w21[0] = 0.95  # wartosci poczatkowe dla warstwy drugiej
    w22[0] = -0.92

    # Algorytm liczenia dla n epok

    for i in range(n):
        dw111[i] = 0  # zerowanie przyrostowwag
        dw112[i] = 0
        dw121[i] = 0
        dw122[i] = 0

        dw1s2[i] = 0  # zerowanie  przyrostow    wag    skosnych
        dw2s2[i] = 0
        dw3s1[i] = 0
        dw4s1[i] = 0

        dw21[i] = 0  # zerowanie   przyrostow   wag   w    warstwie   drugiej
        dw22[i] = 0

        bb[i] = 0  # zerujemy    wektor    pomocnicze
        yy21[i] = 0  # zerujemy   drugi    wektor    pomocniczy

        # dla    kazdego    kroku    obliczeniowego(epoki)    na    wejscie
        # sieci    podajemy    4    wartosci  sygnalow    wejsciowych, w
        # postaci    liczbowej    po    4    wartosci    dla    kazdego
        # wejscia     w    glownej    petli    programu    tej    od
        # 1    do    n    jest    dodatkowa    petla    dla    kazdego
        # sygnalu

        for j in range(learnAndTestCount):  # z11    to    sygnal    po    sumowaniu
            # w    wezle    sumacujnym, przed    funkcja    przejscia     dla
            # jednostki    pierwszej    % zl2    to    sygnal    po    sumowaniu
            # w    wezle    sumacujnym, przed    funkcja    przejscia    dla
            # jednostki    drugiej

            z11 = (u1[j] * w111[i] + u2[j] * w112[i] + u3[j] * w3s1[i] + u4[j] * w4s1[i])
            s11 = (1 / (1 + exp(-z11)))  # to jest sygnal po funkcji przejscia, funkcja sigmoidalna
            z12 = (u3[j] * w121[i] + u4[j] * w122[i] + u1[j] * w1s2[i] + u2[j] * w2s2[i])
            s12 = (1 / (1 + exp(-z12)))  # to jest funkcja sigmoidalna dla drugiej jednostki pierwszej warstwy
            z21 = (s11 * w21[i] + s12 * w22[
                i])  # te sume liczymy tylko raz ponieważ jest tylko jedna % jednsotka w drugiej warstwie sieci
            s21 = (1 / (1 + exp(-z21)))  # to jest sygnal na wyjsciu sieci zatem mozemy

            # obliczac blad sredniokwadratowy, poprzez sumowanie bledu dla 4 wektorow wejsciowych, indeks j dla kazdej epoki indeks i
            # blad sreddniokwadratowy okreslamy jako bb
            bb[i] = bb[i] + 1 / 2 * ((s21 - d[j]) * (
                    s21 - d[j]))  # blad    jako    suma, to    jest    error    na    wyjsciu    z    sieci

            # bedziemy obliczac zmiane wag metoda gradientowa, metoda gradientu prostego
            yy21[i] = yy21[i] + s21 * (1 - s21)
            beta[i] = s21 - d[j]  # pochodna bledu, bo blad jest sredniokwadratowy
            dw21[i] = dw21[i] + s11 * (s21 * (1 - s21)) * beta[i]
            dw22[i] = dw22[i] + s12 * (s21 * (1 - s21)) * beta[i]

            beta21[i] = w21[i] * (s21 * (1 - s21)) * beta[i]
            beta22[i] = w22[i] * (s21 * (1 - s21)) * beta[i]

            # zmiany wag
            dw111[i] = dw111[i] + u1[j] * (s11 * (1 - s11)) * beta21[i]
            dw112[i] = dw112[i] + u2[j] * (s11 * (1 - s11)) * beta21[i]
            dw121[i] = dw121[i] + u3[j] * (s12 * (1 - s12)) * beta22[i]
            dw122[i] = dw122[i] + u4[j] * (s12 * (1 - s12)) * beta22[i]

            dw1s2[i] = dw1s2[i] + u1[0] * (s12 * (1 - s12)) * beta22[i]
            dw2s2[i] = dw2s2[i] + u2[0] * (s12 * (1 - s12)) * beta22[i]
            dw3s1[i] = dw3s1[i] + u3[0] * (s11 * (1 - s11)) * beta21[i]
            dw4s1[i] = dw4s1[i] + u4[0] * (s11 * (1 - s11)) * beta21[i]

            # do optymalizacji zmiany wag stosujemy metode gradientu
            # koniec petli for

        blad[i] = bb[i]

        # liczymy antygradient dla zmiany wagi
        # nowa waga to stara waga - lr * dw[i]
        # nowe wagi:
        w21[i + 1] = w21[i] - lr * dw21[i]
        w22[i + 1] = w22[i] - lr * dw22[i]

        w111[i + 1] = w111[i] - lr * dw111[i]
        w112[i + 1] = w112[i] - lr * dw112[i]

        w121[i + 1] = w121[i] - lr * dw121[i]
        w122[i + 1] = w122[i] - lr * dw122[i]

        w1s2[i + 1] = w1s2[i] - lr * dw1s2[i]
        w2s2[i + 1] = w2s2[i] - lr * dw2s2[i]
        w3s1[i + 1] = w3s1[i] - lr * dw3s1[i]
        w4s1[i + 1] = w4s1[i] - lr * dw4s1[i]
    # koniec petli for

    # --------------------------------------------
    # etap testowania
    wt111 = w111[n]  # wartosci wagi w kroku 101 bo n=100, 100 epok

    wt112 = w112[n]
    wt121 = w121[n]
    wt122 = w122[n]

    wt1s2 = w1s2[n]
    wt2s2 = w2s2[n]
    wt3s1 = w3s1[n]
    wt4s1 = w4s1[n]

    wt21 = w21[n]
    wt22 = w22[n]

    # size = inputVectorCount
    ut1 = [None] * learnAndTestCount
    ut2 = [None] * learnAndTestCount
    ut3 = [None] * learnAndTestCount
    ut4 = [None] * learnAndTestCount
    '''
    ut1[0] = 45.92 / 47.3  # wejscia do testowania dla Asseco
    ut1[1] = 46.32 / 47.3
    ut1[2] = 46.76 / 47.3
    ut1[3] = 47.3 / 47.3

    ut2[0] = 42.59 / 42.88  # wejscia do testowania dla PKO BP
    ut2[1] = 42.88 / 42.88
    ut2[2] = 40.65 / 42.88
    ut2[3] = 41.21 / 42.88

    ut3[0] = 150 / 150  # wejscia do testowania dla Comarch
    ut3[1] = 147 / 150
    ut3[2] = 145 / 150
    ut3[3] = 146.5 / 150

    ut4[0] = 103.6 / 109.8  # wejscia do testowania dla CD Projekt
    ut4[1] = 109.8 / 109.8
    ut4[2] = 108.2 / 109.8
    ut4[3] = 109.5 / 109.8
    '''

    index = 1
    for month in salesData:
        ut1[index - 1], ut2[index - 1], ut3[index - 1], ut4[index - 1] = salesData[month].values()
        index += 1
        if index > learnAndTestCount:
            break


    print("Dane testowania: ", ut1, ut2, ut3, ut4)

    ut1Max = max(ut1)
    ut2Max = max(ut2)
    ut3Max = max(ut3)
    ut4Max = max(ut4)

    for i in range(learnAndTestCount):
        ut1[i] = ut1[i] / ut1Max
        ut2[i] = ut2[i] / ut2Max
        ut3[i] = ut3[i] / ut3Max
        ut4[i] = ut4[i] / ut4Max

    print("Przeskalowane dane testowania: ", ut1, ut2, ut3, ut4)

    # pierwsza suma
    zt11 = ut1[0] * wt111 + ut2[0] * wt112 + ut3[0] * wt3s1 + ut4[0] * wt4s1
    st11 = (1 / (1 + exp(-zt11)))

    zt12 = ut3[0] * wt121 + ut4[0] * wt122 + ut1[0] * wt1s2 + ut2[0] * wt2s2
    st12 = (1 / (1 + exp(-zt12)))

    zt21 = st11 * wt21 + st12 * wt22
    st21 = (1 / (1 + exp(-zt21)))

    # druga suma

    zt11 = ut1[1] * wt111 + ut2[1] * wt112 + ut3[1] * wt3s1 + ut4[1] * wt4s1
    st11 = (1 / (1 + exp(-zt11)))

    zt12 = ut3[1] * wt121 + ut4[1] * wt122 + ut1[1] * wt1s2 + ut2[1] * wt2s2
    st12 = (1 / (1 + exp(-zt12)))

    zt21 = st11 * wt21 + st12 * wt22
    st21 = (1 / (1 + exp(-zt21)))

    # trzecia suma

    zt11 = ut1[2] * wt111 + ut2[2] * wt112 + ut3[2] * wt3s1 + ut4[2] * wt4s1
    st11 = (1 / (1 + exp(-zt11)))

    zt12 = ut3[2] * wt121 + ut4[2] * wt122 + ut1[2] * wt1s2 + ut2[2] * wt2s2
    st12 = (1 / (1 + exp(-zt12)))

    zt21 = st11 * wt21 + st12 * wt22
    st21 = (1 / (1 + exp(-zt21)))

    # czwarta suma
    zt11 = ut1[3] * wt111 + ut2[3] * wt112 + ut3[3] * wt3s1 + ut4[3] * wt4s1
    st11 = (1 / (1 + exp(-zt11)))

    zt12 = ut3[3] * wt121 + ut4[3] * wt122 + ut1[3] * wt1s2 + ut2[3] * wt2s2
    st12 = (1 / (1 + exp(-zt12)))

    zt21 = st11 * wt21 + st12 * wt22
    st21 = (1 / (1 + exp(-zt21)))

    # st21 = st21 * 47.3

    #print(st21 * ut1Max)
    #print(st21 * ut2Max)
    #print(st21 * ut3Max)
    #print(st21 * ut4Max)

    productNames = []
    productValues = [int(st21 * ut1Max), int(st21 * ut2Max), int(st21 *ut3Max), int(st21 * ut4Max)]
    monthResult = None
    resultDict = {}


    for month in salesData:
        monthResult = month
        for product in salesData[month]:
            productNames.append(product)
        break

    print(productNames)
    print(productValues)

    resultDict = {monthResult: {}}

    for i in range(len(productNames)):
        resultDict[monthResult][productNames[i]] = productValues[i]

    print(resultDict)
    return resultDict
    # end of predict


dataDict = {
    'styczen': {'produktA': 100, 'produktB': 120, 'produktC': 154, 'produktD': 200},
    'luty': {'produktA': 100, 'produktB': 210, 'produktC': 189, 'produktD': 220},
    'marzec': {'produktA': 115, 'produktB': 120, 'produktC': 97, 'produktD': 240},
    'kwiecien': {'produktA': 174, 'produktB': 187, 'produktC': 134, 'produktD': 260},
    'maj': {'produktA': 100, 'produktB': 120, 'produktC': 111, 'produktD': 280},
    'czerwiec': {'produktA': 191, 'produktB': 120, 'produktC': 140, 'produktD': 300},
    'lipiec': {'produktA': 180, 'produktB': 120, 'produktC': 150, 'produktD': 320},
    'sierpien': {'produktA': 100, 'produktB': 540, 'produktC': 200, 'produktD': 340},
    'wrzesien': {'produktA': 120, 'produktB': 150, 'produktC': 150, 'produktD': 360},
    'pazdziernik': {'produktA': 100, 'produktB': 120, 'produktC': 120, 'produktD': 380},
    'listopad': {'produktA': 100, 'produktB': 980, 'produktC': 150, 'produktD': 400},
    'grudzien': {'produktA': 130, 'produktB': 120, 'produktC': 50, 'produktD': 420},
}
