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
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props = None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value == None:
            raise ValueError("No value")
        if self.tag == None:
            return self.value
        prop_text = ""
        if self.props != None:
            for prop in self.props:
                prop_text += " " + prop + '="' + self.props[prop] + '"'
        return "<" + self.tag + prop_text + ">" + self.value + "</" + self.tag + ">"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props = None):
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        if self.tag == None:
            raise ValueError("No tag")
        if self.children == None:
            raise ValueError("No children")
        parent_string = "<" + self.tag + ">"
        for child in self.children:
            parent_string += child.to_html()
        parent_string += "</" + self.tag + ">"
        return parent_string