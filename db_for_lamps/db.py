class Lamp:
    def __init__(self, f_text: str, f_img: str | None):
        self.text = f_text
        self.img = f_img


data_for_lamps = {
    1: Lamp(f_text='kerosin_lamp.txt', 
            f_img='kerosin_lamp.jpg'),
    2: Lamp(f_text='aragands_lamp.txt', 
            f_img='argando_lamp.jpg'),
    3: Lamp(f_text='ksenon_lamp.txt',
            f_img='ksenonovaya_lamp.jpg'),
    4: Lamp(f_text='svetodiod_lamp.txt',
            f_img='svetodiod_lamp.jpg')
}