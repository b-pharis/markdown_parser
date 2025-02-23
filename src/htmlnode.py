class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=""):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("to_html method not implemented")
    
    def props_to_html(self):
        props_str = ""
        if not self.props:
            return ""
        for key, value in self.props.items():
            props_str += f' {key}="{value}"'
        return props_str
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
  
    
class LeafNode(HTMLNode):
    def __init__(self, tag=None, value="", props=None):
        if props is None:  # Default to an empty dictionary
            props = {}
        super().__init__(tag, value)
        self.props = props  # Store the props for this instance

    def to_html(self):
        if not self.value:
            raise ValueError("All leafnodes must have a value")
        if self.tag is None:
            return self.value
        if self.props:
            attr_str = " ".join(f'{key}="{value}"' for key, value in self.props.items())
            opening_tag = f"<{self.tag} {attr_str}>"
        else:
            opening_tag = f"<{self.tag}>"

        # Compose and return complete HTML string
        return f"{opening_tag}{self.value}</{self.tag}>" 

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)  # Initialize parent attributes

    
    def to_html(self):
        if not self.tag:
            raise ValueError("All leafnodes must have a tag")
        if len(self.children) == 0:
            raise ValueError("children is a missing list")
        html_children = []
        for child in self.children:
            html_children.append(child.to_html())
        combined_children = "".join(html_children)
        return f"<{self.tag}>{combined_children}</{self.tag}>"
            
    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})" 
    
  