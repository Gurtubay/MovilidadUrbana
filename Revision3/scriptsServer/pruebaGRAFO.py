list=[(0, 24), (1, 24), (13, 24), (14, 24), (22, 24), (23, 24), (0, 23), (1, 23), (13, 23), (14, 23), (16, 23), (17, 23), (22, 23), (23, 23), (3, 22), (21, 22), (12, 20), (18, 20), (3, 19), (0, 18), (1, 18), (6, 18), (7, 18), (13, 18), (14, 18), (0, 17), (1, 17), (6, 17), (7, 17), (13, 17), (14, 17), (10, 16), (2, 15), (5, 15), (18, 14), (9, 13), (0, 12), (1, 12), (6, 12), (7, 12), (13, 12), (14, 12), (16, 12), (17, 12), (22, 12), (23, 12), (0, 11), (1, 11), (6, 11), (7, 11), (12, 11), (13, 11), (17, 11), (18, 11), (22, 11), (23, 11), (0, 9), (1, 9), (6, 9), (7, 9), (12, 9), (13, 9), (17, 9), (18, 9), (22, 9), (23, 9), (0, 8), (1, 8), (6, 8), (7, 8), (13, 8), (14, 8), (16, 8), (17, 8), (22, 8), (23, 8), (10, 7), (21, 5), (5, 4), (12, 4), (19, 2), (0, 1), (1, 1), (6, 1), (7, 1), (13, 1), (14, 1), (16, 1), (17, 1), (22, 1), (23, 1), (0, 0), (1, 0), (6, 0), (7, 0), (13, 0), (14, 0), (16, 0), (17, 0), (22, 0), (23, 0)]

listInt=['DownLeft', 'DownLeft', 'DownLeft', 'DownLeft', 'UpLeft', 'UpLeft', 'DownLeft', 'DownLeft', 'DownLeft', 'DownLeft', 'UpLeft', 'UpLeft', 'UpLeft', 'UpLeft', 'Destination', 'Destination', 'Destination', 'Destination', 'Destination', 'DownLeft', 'DownLeft', 'UpLeft', 'UpLeft', 'DownLeft', 'DownLeft', 'DownLeft', 'DownLeft', 'UpLeft', 'UpLeft', 'DownLeft', 'DownLeft', 'Destination', 'Destination', 'Destination', 'Destination', 'Destination', 'DownLeft', 'DownLeft', 'UpLeft', 'UpLeft', 'DownLeft', 'DownLeft', 'UpLeft', 'UpLeft', 'UpLeft', 'UpLeft', 'DownLeft', 'DownLeft', 'UpLeft', 'UpLeft', 'DownLeft', 'DownLeft', 'UpLeft', 'UpLeft', 'UpLeft', 'UpLeft', 'DownRight', 'DownRight', 'DownRight', 'DownRight', 'DownRight', 'DownRight', 'UpRight', 'UpRight', 'UpRight', 'UpRight', 'DownRight', 'DownRight', 'DownRight', 'DownRight', 'DownRight', 'DownRight', 'UpRight', 'UpRight', 'UpRight', 'UpRight', 'Destination', 'Destination', 'Destination', 'Destination', 'Destination', 'DownRight', 'DownRight', 'DownRight', 'DownRight', 'DownRight', 'DownRight', 'UpRight', 'UpRight', 'UpRight', 'UpRight', 'DownRight', 'DownRight', 'DownRight', 'DownRight', 'DownRight', 'DownRight', 'UpRight', 'UpRight', 'UpRight', 'UpRight']
#print(list)
listaX=[]
listaY=[]
subX=[]
subY=[]
for i in list:
    listaX.append(i[0])
    listaY.append(i[1])
print(len(listaX))
print(len(list))
for i in range(len(list)):
    if listInt[i] == "UpLeft":
        for j in range(len(listaX)):
            if list[i][0] == listaX[j]:
                if listaY[j]-list[i][1] > 1:
                    subY.append(listaY[j]-list[i][1])
                    print("Movimiento vertical")
                    print(str(list[i]))
                    print(str(listaX[j]) +","+str(listaY[j]))
                    print(str(listaY[j]-list[i][1]))
                    print(str(min(subY)))
                    print("-------")
                    #print(subY)
                                
            elif list[i][1] == listaY[j]:
                if list[i][0]-listaX[j] > 1:
                    subX.append(list[i][0]-listaX[j])
                    print("Movimiento horizontal")
                    print(str(list[i]))
                    print(str(listaX[j]) +","+str(listaY[j]))
                    print(str(list[i][0]-listaX[j]))
                    print(str(min(subX)))
                    print("-------")
                    #print(subX)
       # print(len(subY))
        if len(subY)>0:
            if min(subY)>1:
                for k in range(min(subY)):
                    if (list[0]+1,list[1]+k) in list:
                        print("Destination")
                        print(str(list[i]))
                        print(str((list[0]+1,list[1]+k)))
                    elif (list[0]-1,list[1]+k) in list:
                        print("Destination")
                        print(str(list[i]))
                        print(str((list[0]-1,list[1]+k)))
        if len(subX)>0:
            if min(subX)>1:
                for k in range(min(subX)):
                    if (list[i][0]-k,list[i][1]+1) in list:
                        print("Destination")
                        print(str(list[i]))
                        print(str((list[i][0]-k,list[i][1]+1)))
                    elif (list[i][0]-k,list[i][1]-1) in list:
                        print("Destination")
                        print(str(list[i]))
                        print(str((list[i][0]-k,list[i][1]-1)))

            """
    elif listInt == "UpRight":
        print("Int")
    elif listInt == "DownRight":
        pritn("Int")
    elif listInt == "DownLeft":
        print("Int")
        """

