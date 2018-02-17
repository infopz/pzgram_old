# Vecchia versione
# pzGram
A pz-way to create your telegram Bot



ISTRUZIONI (ESEMPIO):
```python
import pzgram
bot = pzgram.Bot(BOTKEY)

def hello(chat, message):
    chat.send("Messaggio ricevuto")
    print(message.text)
    
bot.set_commands({"/hello": hello})
if __name__ == "__main__":
    bot.run()
```

Cose da fare in ordine di importanza:
* Usare thread
* Supporto ai gruppi
* Supporto ai canali
