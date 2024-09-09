def apply_text_color(text, color):
    return f"<span style='color:{color}'>{text}</span>"


def apply_tag_style(href, text):
    return f"<a href='{href}' target='_blank'><span class='tag'>{text}</span></a>"
