# pickem-poker-player
Plays up to 4 tables of pick-em poker.

# Requirements
pip install -r requirements.txt 

install win32api https://sourceforge.net/projects/pywin32/files/pywin32/

install tesseract-ocr https://github.com/UB-Mannheim/tesseract/wiki (non experimental version) 

# Usage
Example 4 table version run as 
```python 4_table_player.py```

If you installed tesseract elsewhere than the default path, add "path=path/to/tesseract" in the bot instantiations.

Open 4 instances of pick'em poker, arrange windows such that they take up 1/4th of the screen each, adjust stake, deal cards and run the bot.

![example](https://i.imgur.com/LSoGaAq.png "Logo Title Text 1")
