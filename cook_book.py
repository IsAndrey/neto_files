import json


class Element():
    '''
    Базовый класс для рецептов, ингридиентов,
    книги рецептов и списка покупок.
    '''
    def __init__(self, name, quantity):
        self.name = name
        self.quantity = quantity
        self.content = []

    def __eq__(self, value):
        '''Сравнение по наименованию.'''
        if isinstance(value, Element):
            return self.name == value.name
        elif isinstance(value, str):
            return self.name == value
        else:
            return False

    def set_content(self, data):
        '''Добавляет элемент к списку.'''
        if self.get_len_content() < self.quantity:
            self.content.append(data)
        else:
            print(
                f'Данные {data} не добавлены: ' +
                f'превышение лимита {self.quantity}'
            )

    def get_len_content(self):
        '''Получает количество загруженных элементов.'''
        return len(self.content)

    def get_content(self):
        '''Представляет данные в виде списка.'''
        return [cont.get_content() for cont in self.content]

    def get_name(self):
        '''Получет наименование.'''
        return self.name

    def get_quantity(self):
        '''Получает количество.'''
        return self.quantity

    def content_is_full(self):
        '''Проверяет количество загруженных элементов.'''
        return len(self.content) == self.quantity

    def get_element_of_content(self, name):
        '''Получет элемент данных (списка) по наименованию.'''
        if name in self.content:
            return self.content[self.content.index(name)]
        else:
            return None

    def get_json(self):
        '''Представляет данные в json формате.'''
        return json.dumps(self.get_content(), ensure_ascii=False, indent=2)


class Recipe(Element):
    '''Моделирует рецепт.'''
    def __str__(self):
        return f'Рецепт {self.name}'

    def set_content(self, data):
        '''Добавляет ингридиент в рецепт.'''
        if len(data) == 3 and data[1].strip().isdigit():
            name = data[0].strip()
            quantity = int(data[1].strip())
            measure = data[2].strip()
            super().set_content(Ingredient(name, quantity, measure))
        else:
            print(f'{data} Ингридиент не загружен.')


class Shop_List(Element):
    '''Моделирует список покупок.'''
    def __init__(self, person_count, name='', quantity=0):
        super().__init__(name, quantity)
        self.person_count = person_count

    def __str__(self):
        return self.get_json()

    def __add__(self, value):
        '''Добавляет/обновляет ингридиенты рецепта в списке покупок.'''
        if isinstance(value, Recipe):
            new_content = [
                ingredient for ingredient in value.content
                if ingredient not in self.content
            ]
            update_content = [
                ingredient for ingredient in value.content
                if ingredient in self.content
            ]
            new_value = Shop_List(self.person_count)
            new_value.content = self.content + new_content
            for ingredient in new_value.content:
                if ingredient in update_content:
                    ingredient += value.get_element_of_content(
                        ingredient.get_name()
                    )
            return new_value

    def get_content(self):
        '''представляет список покупок в виде словаря.'''
        return {
            cont.get_name(): {
                'measure': cont.get_measure(),
                'quantity': cont.get_quantity() * self.person_count
            }
            for cont in self.content
        }


class Ingredient(Element):
    '''Моделирует ингридиент в рецепте.'''
    def __init__(self, name, quantity, measure):
        super().__init__(name, quantity)
        self.measure = measure

    def __str__(self):
        return f'Ингридиент {self.name}'

    def __add__(self, value):
        '''Увеличивает количество ингридиента.'''
        print(self, value)
        if isinstance(value, Ingredient):
            self.quantity += value.get_quantity()
            return self

    def get_content(self):
        '''Представляет ингридиент в виде словаря.'''
        return {
            'ingredient_name': self.name,
            'quantity': self.quantity,
            'measure': self.measure
        }

    def get_measure(self):
        '''Получает единицу измерения.'''
        return self.measure


class Cookbook(Element):
    '''Моделирует книгу рецептов.'''
    def __init__(self, name='', quantity=0):
        super().__init__(name, quantity)

    def __str__(self):
        return self.get_json()

    def set_content(self, data):
        '''Добавляет рецепт в книгу рецептов.'''
        self.quantity = self.get_len_content()+1
        super().set_content(data)

    def get_content(self):
        '''Представляет книгу рецептов в виде словаря'''
        return {
            cont.get_name(): cont.get_content() for cont in self.content
        }

    def get_shop_list_by_dishes(self, dishes, person_count):
        '''Получает список ингридиентов по списку блюд и количеству людей.'''
        shop_list = Shop_List(person_count)
        for dish in dishes:
            recipe = self.get_element_of_content(dish)
            if recipe is not None:
                shop_list += recipe
        return shop_list


def load_cook_book(path='data/recipes.txt', encoding='utf-8', sep=' |'):
    '''Загрузка книги рецептов из файла.'''

    name, quantity = '', 0
    current_recipe = None
    cookbook = Cookbook()
    with open(file=path, mode='r', encoding=encoding) as f:
        for line in f:
            if len(name) > 0 and quantity > 0:
                current_recipe = Recipe(name, quantity)
                name, quantity = '', 0

            if (
                isinstance(current_recipe, Recipe) and
                current_recipe.content_is_full()
            ):
                cookbook.set_content(current_recipe)
                current_recipe = None

            text = line.strip()
            if len(text) == 0:
                next
            if name == '' and current_recipe is None:
                name = text
            elif quantity == 0 and current_recipe is None:
                if text.isdigit():
                    quantity = int(text)
                else:
                    print(
                        f'рецепт {name} не загружен: не найдено количество' +
                        ' ингредиентов.'
                    )
                    name = ''
                    quantity = 0
            else:
                if sep in text and isinstance(current_recipe, Recipe):
                    data = text.split(sep)
                    current_recipe.set_content(data)
        else:
            if (
                isinstance(current_recipe, Recipe) and
                current_recipe.content_is_full()
            ):
                cookbook.set_content(current_recipe)
                current_recipe = None
    return cookbook


if __name__ == '__main__':
    cookbook = load_cook_book()
    print(cookbook)
    print(
        cookbook.get_shop_list_by_dishes(
            dishes=['Фахитос', 'Омлет', 'Утка по-пекински'],
            person_count=4
        )
    )
