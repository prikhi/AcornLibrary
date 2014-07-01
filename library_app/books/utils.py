def tags_from_strings(tag_string):
    return [t.strip() for t in tag_string.split('%') if t.strip()]


def string_from_tags(tags):
    return '%'.join(t.name for t in tags)
