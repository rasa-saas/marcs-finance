from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher

# Base pizza name + description per (dietary preference, topping style).
BASE_PIZZAS = {
    ("meat", "pepperoni_classic"): (
        "Classic Pepperoni",
        "A timeless favorite loaded with pepperoni and melted mozzarella.",
    ),
    ("meat", "meat_lovers"): (
        "Meat Lovers Supreme",
        "Piled high with pepperoni, sausage, bacon, and ham.",
    ),
    ("meat", "bbq_chicken"): (
        "BBQ Chicken Blaze",
        "Grilled chicken, red onion, and tangy bbq sauce in place of tomato sauce.",
    ),
    ("vegetarian", "classic_margherita"): (
        "Margherita Classic",
        "Fresh tomato, mozzarella, and basil — simple and satisfying.",
    ),
    ("vegetarian", "loaded_veggie"): (
        "Loaded Veggie Garden",
        "Bell peppers, mushrooms, onions, olives, and sweet corn.",
    ),
    ("vegetarian", "cheese_lovers"): (
        "Four Cheese Delight",
        "Mozzarella, parmesan, gorgonzola, and provolone all in one bite.",
    ),
    ("vegan", "roasted_vegetables"): (
        "Roasted Vegetable Harvest",
        "Oven-roasted seasonal vegetables over a herby tomato base.",
    ),
    ("vegan", "vegan_cheese_and_herbs"): (
        "Vegan Herb & Cheese",
        "Dairy-free cheese with a generous sprinkle of fresh herbs.",
    ),
    ("vegan", "spicy_plant_based"): (
        "Spicy Plant-Based Fiesta",
        "Plant-based spicy crumbles with jalapenos and a kick of chili oil.",
    ),
}

SPICE_PREFIX = {
    "mild": "",
    "medium": "Zesty ",
    "spicy": "Fire-Breathing ",
}

CRUST_SUFFIX = {
    "thin": "on a thin, crispy crust",
    "deep_dish": "in a thick, Chicago-style deep dish",
    "stuffed": "with a gooey cheese-stuffed crust",
    "gluten_free": "on a gluten-free crust",
}

TOPPING_STYLE_SLOTS = {
    "meat": "pizza_meat_topping_style",
    "vegetarian": "pizza_veggie_topping_style",
    "vegan": "pizza_vegan_topping_style",
}


class ActionRecommendPizza(Action):
    def name(self) -> Text:
        return "action_recommend_pizza"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        dietary_preference = tracker.get_slot("pizza_dietary_preference")
        topping_style_slot = TOPPING_STYLE_SLOTS.get(dietary_preference)
        topping_style = (
            tracker.get_slot(topping_style_slot) if topping_style_slot else None
        )
        spice_level = tracker.get_slot("pizza_spice_level") or "mild"
        crust_style = tracker.get_slot("pizza_crust_style") or "thin"

        base_name, base_description = BASE_PIZZAS.get(
            (dietary_preference, topping_style),
            ("Chef's Choice", "A crowd-pleasing pizza built to order."),
        )

        pizza_name = f"{SPICE_PREFIX.get(spice_level, '')}{base_name}"
        crust_phrase = CRUST_SUFFIX.get(crust_style, "on your favorite crust")
        description = f"{base_description} Served {crust_phrase}."

        return [
            SlotSet("recommended_pizza_name", pizza_name),
            SlotSet("recommended_pizza_description", description),
        ]
