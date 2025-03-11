class HTMLNode():
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    def to_html(self):
        raise NotImplementedError()
    def props_to_html(self):
        string_attr = ""
        for prop in self.props:
            string_attr += prop + '="' + self.props[prop] + '" '
        string_attr = string_attr.rstrip()
        return string_attr
    def __repr__(self):
        return f"Tag: {self.tag}\nValue: {self.value}\nChildren: {self.children}\nProps: {self.props}"