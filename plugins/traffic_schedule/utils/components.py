from linebot.models import BoxComponent, TextComponent


def create_box_component() -> BoxComponent:
    return BoxComponent(layout="horizontal")


def create_text_component(text="") -> TextComponent:
    return TextComponent(text=text)
