#!/usr/bin/env python3

import string
import argparse
import os

description="""Author: Fabian Murer\

Decrypts cipher text which has been encrypted using the Solitaire Cipher.
Find description of the Cipher here: https://www.schneier.com/academic/solitaire/"""

parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description=description)
parser.add_argument('-c', '--cipher', type=str, help='the ciphertext', required=True)
parser.add_argument('-d', '--deck', required=True, help="""Path to the deck file. The deck file describes the key and consists of 54 lines with the card information, e.g.\n
						ca: ace of clubs,\n
						d2: two of diamonds,\n
						h3: three of hearts,\n
						s5: five of spades,\n
						j(r/b): red/black joker""")

args = parser.parse_args()
if not args.cipher or not args.deck:
	parser.print_help()
	exit(1)

alphabet = string.ascii_uppercase
cards = ["ca", "c2", "c3", "c4", "c5", "c6", "c7", "c8", "c9", "c10", "cj", "cq", "ck",
			"da", "d2", "d3", "d4", "d5", "d6", "d7", "d8", "d9", "d10", "dj", "dq", "dk",
			"ha", "h2", "h3", "h4", "h5", "h6", "h7", "h8", "h9", "h10", "hj", "hq", "hk",
			"sa", "s2", "s3", "s4", "s5", "s6", "s7", "s8", "s9", "s10", "sj", "sq", "sk"]

#CIPHER = 'GTIFL RVLEJ TAVEY ULDJO KCCOK P'.replace(' ', '')
CIPHER = args.cipher
CIPHER = CIPHER.replace(' ','')

a_joker = 'jr'
b_joker = 'jb'

SIZE = 54

def get_Deck(path):
	with open(path, 'r') as file:

		deck = []

		for line in file:
			deck.append(line.replace('\n', ''))

		return deck


def convert_text_to_number(text):

	numbered_string = ''
	for c in text:
		if not c == ' ':
			numbered_string += str(alphabet.index(c) + 1)

		numbered_string += " "

	return numbered_string

def convert_number_to_test(array):
	plain = ''

	for n in array:
		c = alphabet[n-1]
		plain += c

	return plain

def convert_card_to_number(card):

	if not (card == a_joker or card == b_joker):
		return cards.index(card) + 1
	else:
		return 53

def move_card(deck, index, step):
	new_index = index + step
	
	if new_index >= SIZE:
		new_index -= SIZE
		new_index += 1

	deck.insert(new_index, deck.pop(index))
	return deck

def gen_keystream_letters(deck):

	key_stream = ''
	counter = 0

	while counter < len(CIPHER):
	
		'''
		STEP 1
		'''
		i = deck.index(a_joker)
		
		deck = move_card(deck, i, 1)

		'''
		STEP 2
		'''
		i = deck.index(b_joker)

		deck = move_card(deck, i, 2)

		'''
		STEP 3
		'''
		index_a = deck.index(a_joker)
		index_b = deck.index(b_joker)

		top = min(index_a, index_b)
		bottom = max(index_a, index_b)

		upper = deck[:top]
		middle = deck[top:bottom+1]
		under = deck[bottom+1:]

		deck = under + middle + upper

		'''
		STEP 4
		'''
		last_card = deck[-1]

		if not(last_card == a_joker or last_card == b_joker):
			number = convert_card_to_number(last_card)

			upper = deck[:number]
			middle = deck[number:-1]

			deck = middle + upper + [last_card]

		'''
		STEP 5
		'''
		top_card = deck[0]
		number = convert_card_to_number(top_card)
		output_card = deck[number]
		
		if output_card == a_joker or output_card == b_joker:
			continue

		'''
		STEP 6
		'''
		key_number = convert_card_to_number(output_card)

		key_stream += str(key_number) + ' '

		counter += 1

	return key_stream

def main():
	DECK = get_Deck(args.deck)

	KEY_STREAM = gen_keystream_letters(DECK)
	KEY_STREAM = KEY_STREAM.split(' ')
	KEY_STREAM = list(filter(None, KEY_STREAM))

	CIPHER_NUMBER = convert_text_to_number(CIPHER)
	CIPHER_NUMBER = CIPHER_NUMBER.split(' ')
	CIPHER_NUMBER = list(filter(None, CIPHER_NUMBER))

	plain = [int(x) - int(y) for x,y in zip(CIPHER_NUMBER, KEY_STREAM)]
	plain = [x % 26 for x in plain]

	print("Cipher Text: {}".format(CIPHER))
	print("Plain Text: {}".format(convert_number_to_test(plain)))

if __name__ == '__main__':
	main()
