class Element():
    def __init__(self, name, quantity):
        self.name = name
        self.quantity = quantity
        self.content = []

    def set_content(self):
        ...


class Recipe(Element):
    def set_content(self, data):
        for i in range(self.quantity):
            name = data[i][1]
            quantity = data[i][2]
            measure = data[i][3]
            self.content.append(Ingredient(name, quantity, measure))


class Ingredient(Element):
    def __init__(self, name, quantity, measure):
        super().__init__(name, quantity)
        self.measure = measure

class Cookbook(Element):
    def __init__(self, file_path, encoding = 'utf-8'):
        self.file_path = file_path
        self.encoding = encoding

    def set_content(self):
        with open(file=self.file_path, mode='r', encoding=self.encoding) as f:
            name = ''
            quantity = 0
            for line in f:
                text = line.strip()
                if len(text) == 0:
                    next
                if name == '':
                    name = text

def load_cook_book(path='data/recipes.txt', encoding='utf-8'):
    def read_recipe(text, current_string):
        ...
    with open(path, 'r', encoding=encoding) as file:
        for line in file:
            text = line.strip()
            print(text)

if __name__ == '__main__':
    load_cook_book()
