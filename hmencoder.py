import sys

char_count = {} # dictionary to store character counts
def read_file(fn):  # read file line by line & store count of each character in dictionary
  charString = ""
  try:
    with open(fn, "r") as f:
      for x in f:
        for c in x:
          charString += c
          if c in char_count:
            char_count[c] += 1
          else:
            char_count[c] = 1
      return charString      
  except IOError:
    print("Cannot read file ", fn)
    exit()

class Node: # create Node class
  def __init__(self, c, v, left, right):
    self.left = left
    self.right = right
    self.c = c
    self.v = v

nodeInfo = [] # list to store info for all the nodes
def Huffman(char_count): # Huffman code
  for i in range(len(char_count)-1):
    min1 = min(char_count.values()) # get the key with lowest count for left node
    minList = [] # index 0 represents left node 1 presents right node
    tempList = [] # minList but string sorted
    temp2List = [] # storing order sorted but string unsorted minList
    for key in char_count:
      if char_count[key] == min1:
        tempList.append(''.join(sorted(key)))
        temp2List.append(key)    
    tempList = sorted(tempList, key=lambda s: ord(s[0])) # sorted by leftmost (smallest character) ASCII value
    if len(tempList) > 1: # if >1 keys with lowest count pick the 2 with least ASCII values as left node and right node
      for i in temp2List: # use letter with smallest ASCII value to represent subtree & re-arrange
       for j in range(len(i)):
          if i[j] == tempList[0][0]:
              minList.append(i)
      for i in temp2List:
       for j in range(len(i)):
          if i[j] == tempList[1][0]:
              minList.append(i)
      leftNode = Node(minList[0], min1, None, None)
      rightNode = Node(minList[1], min1, None, None)        
      char_count.pop(minList[0])
      char_count.pop(minList[1])
      newNode = Node(minList[0]+minList[1], min1*2, leftNode, rightNode)
      # debug
      #print(tempList)
      #print(temp2List)
      #print(minList)  

    else: # pick key with 2nd lowest count using the same method to set as right node
      for i in temp2List:
       for j in range(len(i)):
          if i[j] == tempList[0][0]:
              minList.append(i)
      char_count.pop(minList[0])
      #print(tempList)
      #print(temp2List)
      min2 = min(char_count.values())
      tempList = []
      temp2List = []
      for key in char_count:
        if char_count[key] == min2:
            tempList.append(''.join(sorted(key)))
            temp2List.append(key)
      tempList = sorted(tempList, key=lambda s: ord(s[0]))
      for i in temp2List:
       for j in range(len(i)):
          if i[j] == tempList[0][0]:
              minList.append(i)
      char_count.pop(minList[1])
      tempList = []
      tempList.append(''.join(sorted(minList[0])))
      tempList.append(''.join(sorted(minList[1])))
      tempList = sorted(tempList, key=lambda s: ord(s[0]))
      temp2List = [minList[0], minList[1]]
      minList = []
      for i in temp2List: # use letter with smallest ASCII value to represent subtree & re-arrange
       for j in range(len(i)):
          if i[j] == tempList[0][0]:
              minList.append(i)
      for i in temp2List:
       for j in range(len(i)):
          if i[j] == tempList[1][0]:
              minList.append(i)        
      leftNode = Node(minList[0], min1, None, None)
      rightNode = Node(minList[1], min2, None, None)
      newNode = Node(leftNode.c + rightNode.c, leftNode.v + rightNode.v, leftNode, rightNode)
      #print(tempList)
      #print(temp2List)
      #print(minList)
      #print(min1, min2)    

    nodeRemove = [] # list of previously used left node and right node to remove
    for i in range(len(nodeInfo)):
        if nodeInfo[i].c == minList[0]:
            newNode.left = nodeInfo[i]
            nodeRemove.append(nodeInfo[i])
            break

    for i in range(len(nodeInfo)):
        if nodeInfo[i].c == minList[1]:
            newNode.right = nodeInfo[i]
            nodeRemove.append(nodeInfo[i])
            break

    char_count[newNode.c] = newNode.v # add new node/subtree & its total weight to dictionary char_count        
    for node in nodeRemove:
        nodeInfo.remove(node)
    nodeInfo.append(newNode) # preserve node information

  # nodeInfo[0] is the root
  return nodeInfo[0]
  
def traverseTree(root, code): # recursive generate all codes for all characters & store in dictionary codeInfo
    if root.left is not None:
        traverseTree(root.left, code + "0")
    if root.right is not None:
        traverseTree(root.right, code + "1")
    if len(root.c) == 1:
        codeInfo[root.c] = code

def bitUsed(charString): # calculate total number of bit used in charString according to codeInfo
   b = 0
   for char in charString:
      b += len(codeInfo[char])
   return b   

def writeCode(): # make code.txt 
   with open("code.txt", "w") as f:
     for i in charList:
        f.write(codeInfo[i])
        f.write("\n") 
     f.write(str(round(b/s, 5)))

def writeMsg(charString): # make encodemsg.txt
   encodeString = ""
   for char in charString:
      encodeString+= str(codeInfo[char])
   with open("encodemsg.txt", "w") as f:
        f.write(encodeString)

# main
filename=sys.argv[1]
charString = read_file(filename)
charList = sorted(list(char_count.keys()))
root = Huffman(char_count)
code = ""
codeInfo = {} # dictionary to store code for each character
traverseTree(root, code)
s = next(iter(char_count.values())) # total number of characters
b = bitUsed(charString) # total number of bit used
writeCode()
writeMsg(charString)