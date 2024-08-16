# Tool Base Class
class ToolBase:
    def use(self, query):
        raise NotImplementedError("ToolBase subclasses must implement use method")