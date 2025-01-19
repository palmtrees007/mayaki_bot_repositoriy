class Lamp:
    def __init__(self, f_text: str, f_img: str | None):
        self.text = f_text
        self.img = f_img


class Mayak:
    def __init__(self, f_text: str, f_img: str | None, f_map: str, caption: str):
        self.text = f_text
        self.img = f_img
        self.map = f_map
        self.caption = caption


data_for_mayaks = {
    1: Mayak(f_text='his_hersones.txt',
             f_img='hersones_mayak.jpg',
             f_map='hersones_link.txt',
             caption='Херсонеский маяк'),
    2: Mayak(f_text='his_inkermanskie.txt',
             f_img='inkermanskie.jpg',
             f_map='inkermanskie_link.txt',
             caption='Инкерманские маяки'),
    3: Mayak(f_text='his_sarich.txt',
             f_img='Sarich.jpeg',
             f_map='sarich_link.txt',
             caption='Маяк на мысе Сарыч')
}


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