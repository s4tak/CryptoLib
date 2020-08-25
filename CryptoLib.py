from random import randint

TEXT_CHARACTERS = (10061, 43487, 49669, 74287, 98953, 75767, 74099, 12457, 32159, 53897, 41263, 60331, 91291, 33403, 43651, 40559, 13921, 40531, 37861, 76091, 77093, 80107, 79861, 91801, 93937, 90397)
TEXT_NUMBERS = (42683, 10037, 20101, 49121, 33151, 17029, 58013, 89867, 91199, 97259)
TEXT_SPACE = 99989

KEYS_CHARACTERS = (59077, 77447, 46061, 20897, 48673, 78571, 65963, 15161, 64399, 45497, 91129, 80429, 17377, 42013, 19183, 23099, 22699, 55457, 84871, 84659, 32569, 80777, 52289, 86111, 86291, 37781)
KEYS_NUMBERS = (39443, 89963, 85691, 79273, 49531, 30713, 63059, 59263, 70489, 26647)
KEY_SPACE = 94687

TEXTS = set(TEXT_CHARACTERS + TEXT_NUMBERS + (TEXT_SPACE,))
KEYS = KEYS_CHARACTERS + KEYS_NUMBERS + (KEY_SPACE,)

def readNumbers(filename):
	f = open(filename, "r")
	data = f.read()
	f.close()
	return tuple(map(int, data.split("\n")))


TEXT_CHARACTERS_V4 = readNumbers("texts.txt")
KEYS_CHARACTERS_V4 = readNumbers("passwords.txt")

TEXTS_V4 = set(TEXT_CHARACTERS_V4)
KEYS_V4 = KEYS_CHARACTERS_V4[ord("0"):ord("z") + 1] + KEYS_CHARACTERS_V4[ord("0") - 1::-1] + KEYS_CHARACTERS_V4[ord("z") + 1:]

MULTIPLIER = 10**(len(str(TEXT_SPACE)))
MULTIPLIER_V4 = 10**(len(str(TEXT_CHARACTERS_V4[0])))


class CharConverter:

	ORD_A = ord("a")
	ORD_Z = ord("z")
	ORD_0 = ord("0")
	ORD_9 = ord("9")

	def __init__(self, characters, numbers, space):
		if len(characters) != CharConverter.ORD_Z - CharConverter.ORD_A + 1:
			raise ValueError("longitud de la tupla de caracteres errónea")

		if len(numbers) != 10:
			raise ValueError("Longitud de la tupla de números errónea")

		self.characters = characters
		self.numbers = numbers
		self.space = space


	def getNumber(self, character):
		if character == " ":
			return self.space

		n = ord(character)

		if n >= CharConverter.ORD_0 and n <= CharConverter.ORD_9:
			return self.numbers[n - CharConverter.ORD_0]

		elif n >= CharConverter.ORD_A and n <= CharConverter.ORD_Z:
			return self.characters[n - CharConverter.ORD_A]

		else:
			raise ValueError("Caracter no válido")

	def getCharacter(self, number):
		if number == self.space:
			return " "

		elif number in self.numbers:
			return chr(self.numbers.index(number) + CharConverter.ORD_0)

		elif number in self.characters:
			return chr(self.characters.index(number) + CharConverter.ORD_A)

		else:
			raise ValueError("Número no encontrado")


class CharConverterV4:
	def __init__(self, charactersEnc):
		self.charactersEnc = charactersEnc

	def getNumber(self, character):
		return self.charactersEnc[ord(character)]

	def getCharacter(self, number):
		return chr(self.charactersEnc.index(number))


class EncoderDecoder:

	def __init__(self, charConverter, passwordToKeyFunc, multiplier):
		"""
		charConverter: Convertidor de caracteres
		passwordToKeyFunc: Función que devuelve el número que codifica la contraseña
		multiplier: Multiplicador para los desplazamientos de dígitos"""
		if not callable(passwordToKeyFunc):
			raise ValueError("El convertidor de contraseña a clave no es una función")

		self.charConverter = charConverter
		self.passwordToKeyFunc = passwordToKeyFunc
		self.multiplier = multiplier


	def encode(self, text, password):
		"""Codifica el texto que se pasa como parámetro con la contraseña indicada
		text: Texto a codificar
		password: Contraseña para codificar"""
		return textToNumber(text, self.charConverter, self.multiplier) * self.passwordToKeyFunc(password)


	def decode(self, encodedCode, password):
		"""Decodifica el mensaje con la contraseña indicada y devuelve el texto original
		encodedCode: Mensaje a decodificar
		password: Contraseña para decodificar
		numberToResult: Función que devuelve el texto decodificado al pasarle el número que combina el texto codificado y la contraseña"""
		return numberToText(encodedCode // self.passwordToKeyFunc(password), self.charConverter, self.multiplier)


class EncoderDecoderV5(EncoderDecoder):

	def encode(self, text, password):
		encoded = str(super().encode(text, password))
		num1 = randint(0, 9)
		num2 = randint(0, 8)
		if num2 >= num1:
			num2 += 1

		return encoded.replace(str(num1), "f").replace(str(num2), "e")


	def decode(self, encodedCode, password):
		for i in range(10):
			for j in range(9):
				if j >= i:
					j += 1
				try:
					return super().decode(int(encodedCode.replace("f", str(i)).replace("e", str(j))), password)

				except ValueError:
					pass

		raise ValueError("No de ha podido decodificar")


TEXT_CONVERTER = CharConverter(TEXT_CHARACTERS, TEXT_NUMBERS, TEXT_SPACE)
KEY_CONVERTER = CharConverter(KEYS_CHARACTERS, KEYS_NUMBERS, KEY_SPACE)
TEXT_CONVERTER_V4 = CharConverterV4(TEXT_CHARACTERS_V4)
KEY_CONVERTER_V4 = CharConverterV4(KEYS_CHARACTERS_V4)

passwordToKeyV1 = lambda password: sum(map(KEY_CONVERTER.getNumber, password))
passwordToKeyV2 = lambda password: sum((KEY_CONVERTER.getNumber(character) // (pos + 2) for pos, character in enumerate(password)))
passwordToKeyV3 = lambda password: textToNumber(password, KEY_CONVERTER, MULTIPLIER)
passwordToKeyV4 = lambda password: textToNumber(password, KEY_CONVERTER_V4, MULTIPLIER_V4)

encV1 = EncoderDecoder(TEXT_CONVERTER, passwordToKeyV1, MULTIPLIER)
encV2 = EncoderDecoder(TEXT_CONVERTER, passwordToKeyV2, MULTIPLIER)
encV3 = EncoderDecoder(TEXT_CONVERTER, passwordToKeyV3, MULTIPLIER)
encV4 = EncoderDecoder(TEXT_CONVERTER_V4, passwordToKeyV4, MULTIPLIER_V4)
encV5 = EncoderDecoderV5(TEXT_CONVERTER_V4, passwordToKeyV4, MULTIPLIER_V4)


def textToNumber(text, converter, multip):
	"""Devuelve el número correspondiente de concatenar los números devueltos por el convertidor, al pasarle los caracteres de la cadena a transformar
	text: Texto a transformar
	converter: Objeto convertidor de los caracteres
	multip: Número por el que se multipica para las concatenaciones. Debe ser 10**(numero de caracteres del mayor número devuelto por el convertidor)"""
	num = 0
	for elem in text:
		num = num * multip + converter.getNumber(elem)

	return num


def numberToText(num, converter, multip):
	""""""
	decoded = ""

	while num > 0:
		decoded += converter.getCharacter(num % multip)
		num //= multip

	return decoded[::-1]


def main():
	pass


if __name__ == '__main__':
	main()