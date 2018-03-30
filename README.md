# Solitaire Cipher Decrypter

This tool can be used to decrypt a cipher text that has been encrypted using the Solitaire cipher. Find more information about the Solitaire cipher on https://www.schneier.com/academic/solitaire/.

# Install

```bash
git clone https://github.com/fmurer/solitaire_cipher
cd solitaire_cipher
chmod +x solitaire.py
./solitaire.py -c CIPHER_TEXT -d DECK
```

# Format of the Deck

The deck is the key in the Solitaire cipher. The deck needs to be a set of cards consisting of 54 cards (2 jokers). The deck file describes the order of the cards and is therefore a file of 54 lines describing the cards position.

```
da	# ace of diamonds
s2	# two of spades
h3	# three of hearts
c4	# four of clubs
jb	# black joker
jr	# red joker
...
```

# Example
```bash
./solitaire.py -c "GTIFL RVLEJ TAVEY ULDJO KCCOK P" -d ./deck.txt 
Cipher Text: GTIFLRVLEJTAVEYULDJOKCCOKP
Plain Text: THEPASSWORDISCRYPTONOMICON
```
