import heapq

huffman_codes = {}

class node:
	def __init__(self, freq, symbol, left=None, right=None):
		# frequency of symbol
		self.freq = freq

		# symbol name (character)
		self.symbol = symbol

		# node left of current node
		self.left = left

		# node right of current node
		self.right = right

		# tree direction (0/1)
		self.huff = ''
		
	def __lt__(self, nxt):
		return self.freq < nxt.freq
		

# utility function to print huffman
# codes for all symbols in the newly
# created Huffman tree
def printNodes(node, val=''): 
	# huffman code for current node
	newVal = val + str(node.huff)

	# if node is not an edge node
	# then traverse inside it
	if(node.left):
		printNodes(node.left, newVal)
	if(node.right):
		printNodes(node.right, newVal)

		# if node is edge node then
		# display its huffman code
      
	if(not node.left and not node.right):
		print(f"{node.symbol} -> {newVal}")
		huffman_codes[node.symbol] = newVal

           
# open image as binary file
file = open('balloon.jpg', 'rb')
bit_string = ""
byte = file.read(1)
while len(byte) > 0:
    byte = ord(byte)
    bits = bin(byte)[2:].rjust(8,'0')
    bit_string += bits
    byte = file.read(1)
file.close()


# print(bit_string)


# finding frequencies of each byte
frequencies = {}
for i in range(0, len(bit_string), 8):
    # print(bit_string[i:i+8])
    if bit_string[i:i+8] in frequencies:
        frequencies[bit_string[i:i+8]] += 1
    else:
        frequencies[bit_string[i:i+8]] = 1


# print(frequencies)

# sorted bytes by frequencies value
sorted_frequencies = sorted(frequencies.items(), key=lambda x:x[1])
print(sorted_frequencies)



# list containing unused nodes
nodes = []

# converting characters and frequencies
# into huffman tree nodes
for x in range(len(sorted_frequencies)):
	heapq.heappush(nodes, node(sorted_frequencies[x][1], sorted_frequencies[x][0]))

while len(nodes) > 1:
	
	# sort all the nodes in ascending order
	# based on their frequency
	left = heapq.heappop(nodes)
	right = heapq.heappop(nodes)

	# assign directional value to these nodes
	left.huff = 0
	right.huff = 1

	# combine the 2 smallest nodes to create
	# new node as their parent
	newNode = node(left.freq+right.freq, left.symbol+right.symbol, left, right)

	heapq.heappush(nodes, newNode)

# Huffman Tree
printNodes(nodes[0])


# replace huffman code with bit string
bit_string_out = ""
for i in range(0, len(bit_string), 8):
	bit_string_out += huffman_codes[bit_string[i:i+8]]


# convert bit string out to byte array
output = bytearray()
for i in range(0, len(bit_string_out), 8):
	output.append(int(bit_string_out[i:i+8], 2))

# print(output)

# write byte array to .bin file
file = open('balloon_compressed.bin', 'wb')
file.write(output)
file.close()

# print compression ratio
print("CR: ", len(bit_string)/len(bit_string_out))

# ----------------------------------------------------------------------------------------

# decompress
file = open('balloon_compressed.bin', 'rb')
bit_string = ""
byte = file.read(1)
while len(byte) > 0:
    byte = ord(byte)
    bits = bin(byte)[2:].rjust(8,'0')
    bit_string += bits
    byte = file.read(1)
file.close()

bit_string_out = ""
i= 0
pi = -1 
while i < len(bit_string):
	for key in huffman_codes:
		if bit_string[i:i+len(huffman_codes[key])] == huffman_codes[key]:
			bit_string_out += key
			i += len(huffman_codes[key])
			break
	if pi == i:
		break
	pi = i


output = bytearray()
for i in range(0, len(bit_string_out), 8):
	output.append(int(bit_string_out[i:i+8], 2))

# write byte array to file
file = open('balloon_decompressed.jpg', 'wb')
file.write(output)
file.close()