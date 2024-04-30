# full print all data
# remaked by iFanpS; helped by KIPAS (alot of help)
import struct
SECRET = "PBG892FXX982ABC*"
def memcpy(id, nlen, pos, enc, data):
    str = ''
    if enc == True:
        for i in range(nlen):
            str += chr(data[pos])
            pos += 1
    else:
        for i in range(nlen):
            str += chr(data[pos] ^ ord(SECRET[(id + i) % len(SECRET)]))
            pos += 1
    return str
def decFile(data):
    ww = -1
    memPos = 0
    itemsdatVersion = struct.unpack('<H', data[memPos:memPos+2])[0]
    memPos += 2
    itemCount = struct.unpack('i', data[memPos:memPos+4])[0]
    memPos += 4
    yes = False
    for i in range(itemCount):
        itemID = struct.unpack('i', data[memPos:memPos+4])[0]
        memPos += 4
        
        editableType = data[memPos]
        memPos += 1
        itemCategory = data[memPos]
        memPos += 1
        actionType = data[memPos]
        memPos += 1
        hitSoundType = data[memPos]
        memPos += 1
        
        ##name parse
        strLen = data[memPos] + data[memPos + 1] * 256
        memPos += 2
        name = memcpy(itemID,strLen,memPos, False, data)
        memPos += strLen
        ##name parse end
        
        ##texture parse
        strLen = data[memPos] + data[memPos + 1] * 256
        memPos += 2
        texture = memcpy(itemID,strLen,memPos, True, data)
        memPos += strLen
        ##texture parse
        
        #texturehash parse
        textureHash = struct.unpack('i', data[memPos:memPos+4])[0]
        memPos += 4
        #end
        
        #itemKind
        itemKind = data[memPos]
        memPos += 1
        #end
        
        #val1 parse
        val1 = struct.unpack('i', data[memPos:memPos+4])[0]
        memPos += 4
        #end
        
        #textureX & textureY
        textureX = data[memPos]
        textureY = data[memPos]
        memPos += 2
        #end
        
        #spreadType
        spreadType = data[memPos]
        memPos += 1
        #end
        
        #stripeywallpaper
        isStripeyWallpaper = data[memPos]
        memPos += 1
        #end
        
        #Collision
        collisionType = data[memPos]
        memPos += 1
        #end
        
        #breakHits
        breakHits = data[memPos]
        memPos += 1
        #end
        
        #dropChance
        dropChance = struct.unpack('i', data[memPos:memPos+4])[0]
        memPos += 4
        #end
        
        #clothingType 
        clothingType = data[memPos]
        memPos += 1
        #end
        
        #rarity
        rarity = struct.unpack('i', data[memPos:memPos+4])[0]
        memPos += 2
        #end
        
        #maxAmount
        maxAmount = data[memPos]
        memPos += 1
        #end
        
        ##extrFile parse
        strLen = data[memPos] + data[memPos + 1] * 256
        memPos += 2
        extraFile = memcpy(itemID,strLen,memPos, True, data)
        memPos += strLen
        ##extraFile parse
        
        #extraFilehash
        extraFilehash = struct.unpack('i', data[memPos:memPos+4])[0]
        memPos += 4
        #end
        
        #audioVolume
        audioVolume = struct.unpack('i', data[memPos:memPos+4])[0]
        memPos += 4
        #end
        
        ##pet option
        strLen = data[memPos] + data[memPos + 1] * 256
        memPos += 2
        petName = memcpy(itemID,strLen,memPos, True, data)
        memPos += strLen
        
        strLen = data[memPos] + data[memPos + 1] * 256
        memPos += 2
        petPrefix = memcpy(itemID,strLen,memPos, True, data)
        memPos += strLen
        
        strLen = data[memPos] + data[memPos + 1] * 256
        memPos += 2
        petSuffix = memcpy(itemID,strLen,memPos, True, data)
        memPos += strLen
        
        strLen = data[memPos] + data[memPos + 1] * 256
        memPos += 2
        petAbillity = memcpy(itemID,strLen,memPos, True, data)
        memPos += strLen
        ##pet option
        
        #seed(base,overlay)
        seedBase = data[memPos]
        seedOverlay = data[memPos]
        memPos += 2
        #end
        
        #tree(base,leaves)
        treeLeaves = data[memPos]
        treeBase = data[memPos]
        memPos += 2
        #end
        
        #seed(color,overlaycolor)
        seedColor = struct.unpack('i', data[memPos:memPos+4])[0]
        memPos += 4
        seedOverlayColor = struct.unpack('i', data[memPos:memPos+4])[0]
        memPos += 4
        #end
        
        memPos += 4 #deleted ingridients
        
        #growTime
        growTime = struct.unpack('i', data[memPos:memPos+4])[0]
        memPos += 4
        #end
        
        #val2 & isRayman
        val2 = struct.unpack('i', data[memPos:memPos+4])[0]
        memPos += 2
        isRayman = struct.unpack('i', data[memPos:memPos+4])[0]
        memPos += 2
        #end
        
        ##item extra data
        strLen = data[memPos] + data[memPos + 1] * 256
        memPos += 2
        extraOptions = memcpy(itemID,strLen,memPos, True, data)
        memPos += strLen
        
        strLen = data[memPos] + data[memPos + 1] * 256
        memPos += 2
        texture2 = memcpy(itemID,strLen,memPos, True, data)
        memPos += strLen
        
        strLen = data[memPos] + data[memPos + 1] * 256
        memPos += 2
        extraOptions2 = memcpy(itemID,strLen,memPos, True, data)
        memPos += strLen
        
        ##item extra data
        
        memPos += 80; #unknown data
        
        if (itemsdatVersion >= 11):
            strLen = data[memPos] + data[memPos + 1] * 256
            memPos += 2
            punchOptions = memcpy(itemID,strLen,memPos, True, data)
            memPos += strLen
            
        if (itemsdatVersion >= 12):

            memPos += 13
# skip data
        
        if (itemsdatVersion >= 13):
            memPos += 4
# skip data
        
        if  (itemsdatVersion >= 14):
            memPos += 25 # skip data
        ww = ww + 1
        print(str(name))
     #   o = open("test.txt", "a")
     #   a1 = "{"
     #   a2 = "}"
        #print(f"{a1}\"id\":{ww},\"name\":\"{name}\"{a2},\n")
       # if yes == False:
         #o.write(f"{a1}\"itemid\":[")
         #yes = True
       #  o.write(f"{a1}\n")
       #  yes = True
        #o.write(f"{a1}\"id\":{ww},\"name\":\"{name}\"{a2},\n")
       # print(f"\"{ww}\":\"{name}\",\n")
      #  o.write(f"\"{ww}\":\"{name}\",\n")
        #print(f"drop chance {dropChance}")
        #print(f"name {name} textureHash {textureHash}")
        #print(f"texturex {textureX}")
        #print(itemID)
        #{"c":1,"i":18}
# print what you want here        
      #  if i != itemID:
         #   print('Unordered item ' + str(itemID) + '/' + str(itemCount))
    

#a = input('items.dat loc/name: ')
decFile(open("items2.dat", 'rb').read())