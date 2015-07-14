albumen
===========

Collect album art
Arrange and curate it
Analyze it
Create desktops and mosaics of your favorite albums

TODO [features]:
- Use sqilte queries to order images
- Swappable subclasses for image analysis, plus testing framework
- Return analysis objects from storage image calls

TODO [bugs]: 
- A Blaze in the Northern Sky

2015-07-14:
Added in the Spotify hackday stuff. Basic use:
  > python compile.py --uri spotify:user:stuartmershon:playlist:5jXbxp8Ir5UBqKBnFo1ZSo
  
  > python compile.py --uri spotify:user:stuartmershon:playlist:5jXbxp8Ir5UBqKBnFo1ZSo --num 300 --size 1440x900
  
The albumen library needs to be installed first. It also tries to write everything (large image, thumbnail, metadata) in some directories like webapp/static/images and webapp/static/meta, so you will need to either change those or create those directories.


