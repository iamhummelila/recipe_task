#!/usr/bin/env python3
# coding: utf8

"""
Recipe: container for a structured recipe.
"""

from typing import Union, Iterator, Dict


class Recipe:
    """Structured representation of a recipe."""

    def __init__(self, recipe: str):
        self.recipe = recipe
        self.splitted = recipe.split("\n")
        self.text = [i for i in self.splitted if len(i) > 1]
        self.title = self.text[0]
        self.italian_title = self.text[1]
        self.instructions = self.get_instructions()
        self.ingredients = self.get_ingredients()
        self.preptime = self.preptime_minutes()
        self.serving_size = self.set_serving_size()


    def get_instructions(self):
        ind = 4 + len(self.ingredients)
        instructions = self.text[ind:]
        return instructions


    def get_ingredients(self, size=1):
        """
        Returns the ingredients in a dictionary in the following way:
        
        {Ingredient: {unit: no}}
        """
        ing_dict = {}
        for line in self.text[4:]:
            if line.startswith("*"):
                ingred = line.split("\t")
                no = ingred[1]*size
                unit = ingred[2]
                entity = ingred[3]
                ing_dict[entity] = {unit: no}
            return ing_dict


    def preptime_minutes(self):
        preptime = self.text[3]
        the_time = preptime[18:]
        if "hour" in the_time:
            hind = the_time.index("hour")
            hour = the_time[:hind].rsplit(" ") 
            hour = hour.replace(" ", "")
            minutes = hour * 60
            return minutes
        the_time = the_time.replace("minutes", "")
        the_time = the_time.replace(" ", "")
        return the_time


    def get_serving_size(self):
        servings = self.text[2]
        splitted = servings.split(" ")
        size = splitted[0]
        return size


    def __iter__(self) -> Iterator[str]:
        """Iterate over recipe instructions."""
        return iter(self.instructions)

    def __len__(self) -> int:
        """Number of ingredients."""
        return len(self.ingredients)

    def __str__(self) -> str:
        """Get original recipe text."""
        return self.recipe

    def __lt__(self, other:  Union[str, 'Recipe']) -> bool:
        """Compare preparation time of two recipes."""
        return self.preptime < other

    def __gt__(self, other: Union[str, 'Recipe']) -> bool:
        """Compare preparation time of two recipes."""
        return self.preptime > other

    def set_serving_size(self, serving_size: int):
        """Update new serving size."""
        if self.serving_size == serving_size:
            return self.serving_size
        else:
            relation = self.serving_size/serving_size
            self.get_ingredients(size=relation)
            return serving_size

    @classmethod
    def get_shopping_list(cls, *recipes: Union[str, 'Recipe']) -> Dict[str, Dict[str, float]]:
        """Get combined shopping list for a number of recipes"""
        shopping_list = {}
        
        for recipe in recipes:
            ings = recipe.ingredients
            # ings: {Ingredient: {unit: no}}
            for ingred, measure in ings.items():
                number = measure.values()
                if ingred in shopping_list:
                    old_measure = shopping_list(ingred)
                    if measure in old_measure:
                        old_measure[measure] = old_measure(measure) + number
                    else:
                        shopping_list[ingred] = shopping_list(ingred).update(measure)
                else:
                    shopping_list[ingred] = measure

        return shopping_list
