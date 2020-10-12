BOOTSTRAP4 = {
    "include_jquery": True,
    "javascript_in_head": True,
    "css_url": {
        "href": "https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css",
        "integrity": "sha384-JcKb8q3iqJ61gNV9KGb8thSsNjpSL0n8PARn9HuZOnIxN0hoP+VmmDGMN5t9UJ0Z",
        "crossorigin": "anonymous",
    },
    "javascript_url": {
        "url": "https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js",
        "integrity": "sha384-B4gt1jrGC7Jh4AgTPSdUtOBvfO8shuf57BaghqFfPlYxofvL8/KUEfYiJOMMV+rV",
        "crossorigin": "anonymous",
    },
    "jquery_url": {
        "url": "https://code.jquery.com/jquery-3.5.1.min.js",
        "integrity": "sha256-9/aliU8dGd2tb6OSsuzixeV4y/faTqgFtohetphbbj0=",
        "crossorigin": "anonymous",
    },
    "popper_url": {
        "url": "https://cdn.jsdelivr.net/npm/popper.js@1.16.1/dist/umd/popper.min.js",
        "integrity": "sha384-9/reFTGAW83EW2RDu2S0VKaIzap3H66lZH81PoYlFhbGU+6BZp6G7niu735Sk7lN",
        "crossorigin": "anonymous",
    },
}

RECIPE_UNIT_DEFINITIONS = {
    "mL": {"digits": 0},
    "g": {"digits": 0},
    "tablespoon": {"min": 0.0, "max": 10.0, "digits": 2},
    "teaspoon": {"min": 0.0, "max": 10.0, "digits": 2},
    "cup": {"min": 0.0, "max": 10.0, "digits": 2},
}
RECIPE_UNIT_CONVERSIONS = [
    {
        "names": ["water", "milk"],
        "density": 1.0,
        "units": ["mL", "cup", "g", "tablespoon", "teaspoon"],
    },
    {
        "names": ["flour"],
        "density": 0.528344104716297,
        "units": ["cup", "g", "tablespoon", "teaspoon"],
    },
    {
        "names": ["sugar", "brown sugar", "granulated sugar"],
        "density": 0.8453505675460752,
        "units": ["cup", "g", "tablespoon", "teaspoon"],
    },
    {
        "names": ["butter"],
        "density": 0.9594728941647953,
        "units": ["cup", "g", "tablespoon", "teaspoon"],
    },
    {
        "names": ["oil", "vegetable oil", "olive oil", "sunflower oil"],
        "density": 0.918,
        "units": ["mL", "cup", "g", "tablespoon", "teaspoon"],
    },
    {
        "names": ["tomato passata", "tomato sauce"],
        "density": 1.0355182768975872,
        "units": ["mL", "cup", "g", "tablespoon", "teaspoon"],
    },
    {
        "names": ["bulgur"],
        "density": 0.59,
        "units": ["cup", "g", "tablespoon", "teaspoon"],
    },
]
