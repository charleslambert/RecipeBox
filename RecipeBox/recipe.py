from fractions import Fraction
import textwrap


class Recipe:
    def __init__(self, title, ingredients, instructions):
        self.title = title
        self.ingredients = ingredients
        self.instructions = instructions

    @classmethod
    def from_dict(cls, d):
        return cls(d["title"], d["ingredients"], d["instructions"])

    def __str__(self):

        ing_output = ""
        for ingredient in self.ingredients:
            num, den = ingredient["amount"]
            if (num / den) % 1 == 0 or (num / den) < 1:
                formated_amount = "{}".format(str(Fraction(num, den)))
            else:
                formated_amount = "{} {}".format(
                    int(num / den), str(Fraction(int(num / den), den)))

            ing_output += "  {:>5} {:<10}{:<}\n".format(
                formated_amount, ingredient["measure"], ingredient["name"])

        ins_output = ""
        for i, instruction in enumerate(self.instructions):
            wrapped_lines = textwrap.wrap(instruction)
            ins_output += " {:>2}: {}\n".format(i + 1, wrapped_lines[0])
            for line in wrapped_lines[1:]:
                ins_output += "     {}\n".format(line)
            ins_output += "\n"

        return "\n{}\n\n{}\n{}\n".format(self.title, ing_output, ins_output)
