# Desk-Emoji

Desk-Emoji is a truly open-source AI desktop robot featuring an emoji screen, a two-axis console, and LLM capabilities for voice chat. ( [Demo](https://www.bilibili.com/video/BV1GnsdePEaz/) )

![](images/photo.jpg "photo")

## Installation

### Hardware

* Assamble 2 axis servos:
  ![img](images/servo.jpg "servo")
* OLED display connection:
  ![img](images/oled.jpg "oled")

### Software

* 3.9 <= Python version <= 3.11
* Initialize environment

  * For MacOS or Linux:

    * `./init.sh`
    * `source .venv/bin/activate`
  * For Windows:

    * `.\init.bat`
    * `.venv\Scripts\activate`
* Launch the main program

  * `python main.py`
  * ![1730990829645](images/gui.png)
* Test robot

  * Test action: `python action.py`
  * Test chat:  `python chat.py`

## Author

* Mark Yang
* Email: mark.yang@ewen.ltd
