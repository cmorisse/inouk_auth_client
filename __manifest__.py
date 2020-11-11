{
    "name": "inouk_auth_client",
    "summary": """ Add Odoo Inouk Auth as second Auth factor for Odoo """,
    "author": "Cyril MORISSE - @cmorisse",
    "category": "Uncategorized",
    "license": "LGPL-3",
    "version": "13.0.1.0.0",
    "images": [
    ],
    "installable": True,
    "depends": [
        "web",
    ],
    "data": [
    ],
    "external_dependencies": {
        "python": [
            "requests_hawk",  # pip install requests-hawk==1.0.1
        ],
    },
}
