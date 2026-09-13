print('x,w,z,y')
for x in range(2):
    for y in range(2):
        for w in range(2):
            for z in range(2):
                F = (x and (not y )) or (y == z) or w
                if F == 0:
                    print(x,w,z,y)
    
    