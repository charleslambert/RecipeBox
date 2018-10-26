import textwrap
from fractions import Fraction

import click

from prompts import amount_prompt, list_items, sanitized_input, y_n_prompt, measure_prompt
from recipe import Recipe
from store import Store


def to_tuple(fraction):
    return (fraction.numerator, fraction.denominator)


def new_recipe():
    recipe = {"title": "", "ingredients": [], "instructions": []}

    recipe["title"] = input("Recipe Name:\n  ")

    while True:
        ingredient = {}
        plural = False

        print("Add an ingredient:")

        ingredient["name"] = sanitized_input("  Name: ", str)
        ingredient["amount"] = amount_prompt("  Amount: ")
        if ingredient["amount"] > 1:
            ingredient["amount"] = to_tuple(ingredient["amount"])
            plural = True
        ingredient["measure"] = measure_prompt("  Measurment: ", plural)
        recipe["ingredients"].append(ingredient)

        if y_n_prompt("Add more ingredients", "n") == "n":
            break
    while True:
        print("Add an instruction:")
        recipe["instructions"].append(sanitized_input("  Instruction: ", str))

        if y_n_prompt("Add more instructions", "n") == "n":
            break

    return recipe


def print_recipe(recipe):
    print("\n{}\n".format(recipe["title"]))
    for ingredient in recipe["ingredients"]:
        num, den = ingredient["amount"]
        if (num / den) % 1 == 0 or (num / den) < 1:
            formated_amount = "{}".format(str(Fraction(num, den)))
        else:
            formated_amount = "{} {}".format(
                int(num / den), str(Fraction(int(num / den), den)))

        print("  {:>5} {:<10}{:<}".format(
            formated_amount, ingredient["measure"], ingredient["name"]))

    print()
    for i, instruction in enumerate(recipe["instructions"]):
        wrapped_lines = textwrap.wrap(instruction)
        print(" {:>2}: {}".format(i + 1, wrapped_lines[0]))
        for line in wrapped_lines[1:]:
            print("     {}".format(line))
        print()


@click.command()
def main():
    store = Store()
    recipes = store.load()
    recipes = [Recipe.from_dict(x) for x in recipes]
    while True:
        selection = list_items("Recipe Box",
                               ["Add a recipe", "Read a recipe", "Quit"])

        if selection == 0:
            recipes.append(new_recipe())
            store.save(recipes)

        if selection == 1:
            r = list_items("Recipes", [recipe.title for recipe in recipes])
            print(recipes[r])

        if selection == 2:
            break


if __name__ == '__main__':
    main()
