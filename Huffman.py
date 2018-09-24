# Huffman Encoding
from collections import deque
def get_freq(words):
    """
    Given a string words, returns a dictionary with the frequency
    of each character in the string called words. 
    """
    dic = {words[i]:0 for i in range(len(words))}
    for i in range(len(words)):
        dic[words[i]] = dic[words[i]] + 1
    return dic

def get_2_min(q):
    """
    Helper function to get two minimum elements in the list of
    nodes sorted on the basis of their frequency.
    """
    s = sorted(q,key = lambda node: node.freq)
    return s[0],s[1]

# The node class is the basic structure
# of each node present in the huffman - tree.
class HuffmanNode:
    def __init__(self,data,freq):
        self.data = data
        self.freq = freq
        self.left = None
        self.right = None
        
 
def makeCode(root,string,dic = {}):
    """
    Recursive function to print the tree.
    Here the string is the huffman code generated
    The dictionary dic get's the code for each string.
    """
    #Base case
    # If the left and the right of the root are none
    # Then it is a leaf node so we just print its value
    if root.left == None and root.right == None:
        # Make the string its Huffman Code for future use
        dic[root.data] = string
        return dic

    # if we go to left then add "0" to the code.
    # if we go to the right add "1" to the code.
    
    makeCode(root.left, string+"0",dic)
    makeCode(root.right, string+"1",dic)

def makeHuffmanTree(string):
    """
    Given a string make a Huffman Tree.
    The function returns the root of the Huffman Tree.
    """
    frequency = list(get_freq(string).items())
    # Make a queue of Huffman Nodes
    q = deque()
    for i in range(len(frequency)):
        h = HuffmanNode(frequency[i][0],frequency[i][1])
        h.left = None
        h.right = None
        q.append(h)
    root = None     
    while len(q) > 1:
        # Get the first two minimum elements 
        node1,node2 = get_2_min(q)
        q.remove(node1)
        q.remove(node2)
        # Make Huffman Node and a parent
        parent = HuffmanNode('-',node1.freq+node2.freq)
        parent.left = node1
        parent.right = node2
        # Make the parent the current root
        root = parent
        # Add the parent to the q to make the tree
        q.append(parent)
    return root

def encode_huffman(file):
    """
    Given file name the function will create/overwrite a file
    with name "Huffman"+fileName which will be encoded in Huffman Code. 
    """
    f = open(file,'r')
    s = ""
    for line in f.readlines():
        s = s + line
    f.close()
    # Convert the file text into a giant string
    # And make a Huffman Tree out of it
    root = makeHuffmanTree(s)
    # Get a dictionary that stores the codes
    dic = {}
    makeCode(root,"",dic)

    ####################################################################
    # For debugging one can print the codes to see if they are correct
    # print(dic)
    ###################################################################
    
    # Make a new encoded file
    code_file = open("Huffman "+file,'w')
    # Make an encoded string
    enc_s = ""
    # Replace each character by it Huffman Code.
    for char in s:
        enc_s = enc_s + str(dic[char])
    code_file.write(enc_s)
    code_file.close()

def decode_huffman(huf_file,frequency):
    file = open(huf_file,'r')
    # Get the entire Huffman code in string s. 
    s = ""
    for line in file.readlines():
        s += line
    file.close()

    # Making a Huffman Tree like before.
    # This part can be improved by making a sperate method. The previous method uses the string(decoded) to make
    # Huffman Tree. So it cannot be used here.
    
    # Make a queue of Huffman Nodes
    q = deque()
    for x,y in frequency.items():
        h = HuffmanNode(x,y)
        h.left = None
        h.right = None
        q.append(h)
    root = None     
    while len(q) > 1:
        # Get the first two minimum elements 
        node1,node2 = get_2_min(q)
        q.remove(node1)
        q.remove(node2)
        # Make Huffman Node and a parent
        parent = HuffmanNode('-',node1.freq+node2.freq)
        parent.left = node1
        parent.right = node2
        # Make the parent the current root
        root = parent
        # Add the parent to the q to maake the tree
        q.append(parent)
    # Once the tree is made we can start decoding the string. 
    decoded_string = ""
    cur = root
    # For each element in string s do a tree traversal depending on its value.  
    for i in range(len(s)):
        if s[i] == '0':
            cur = cur.left
        else: 
            cur = cur.right
        # leaf nodes contain the character corresponding to a certain huffman code. 
        if cur.left == None and cur.right == None:
            decoded_string += cur.data
            cur = root
    
    new_file = open('Decoded '+huf_file,'w')
    new_file.write(decoded_string)
    new_file.close()
    
    


f = open('random_text.txt','r')
s = ""
for line in f.readlines():
    s = s + line
f.close()
frequency = get_freq(s)

# Testing
# Encode the file with name, random_text.txt
encode_huffman('random_text.txt')
# Decode the file with name Huffman random_text.txt
decode_huffman('Huffman random_text.txt',frequency)
# To compare file size
import os
print("File size before Huffman Encoding (in bytes): ",os.stat('random_text.txt').st_size)
print("File size after Huffman Encoding (in bytes): ",os.stat('Huffman random_text.txt').st_size)
