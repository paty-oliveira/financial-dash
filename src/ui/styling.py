def apply_text_color(text, color):
    return f"<span style='color:{color}'>{text}</span>"


def apply_link_style(href, text):
    return f"<a href='{href}' target='_blank'><span class='tag'>{text}</span></a>"


def apply_tag_style(text):
    return f"<span class='link'>{text}</span>"
