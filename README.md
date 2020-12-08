# CryptoLib

_Una librería para el manejo de el cifrado simétrico DS(1-5)_


## Uso 🔧

<a href="https://ibb.co/Vg1rXqK"><img src="https://i.ibb.co/K2PRCr1/unknown.png" alt="unknown" border="0"></a>

```
import CryptoLib

string=("My secret")
ciphertext=CryptoLib.encV5.encode(string, "1234")
plaintext=CryptoLib.encV5.decode(ciphertext, "1234")
print(plaintext)
```

## Advertencias ⚠️

DS es un algoritmo de cifrado que no está verificado como seguro, no se recomienda su uso. Tenga en cuenta que ha sido desarrollado por diversión, por favor no lo utilice en algo que requira seguridad.


## Autores ✒️


* **s4tak** - (https://github.com/s4tak)
* **dan884074** - (https://github.com/dan884074)

