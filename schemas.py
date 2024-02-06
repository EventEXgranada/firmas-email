from schema import Schema, Optional, And

S_CONFIG = Schema(
    {
        "id": str,
        "output_path": str,
        "main_font": str,
        "name_font": str,
        "name_image": str,
        "color": str,
        "organization": str,
        Optional("organization_extra"): str,
        Optional("phone"): str,
        Optional("phone_country_code"): str,
        Optional("internal_phone"): str,
        Optional("opt_mail"): str,
        Optional("max_width"): int,
        Optional("links"): [
            {
                "url": str,
                "image": str,
                "alt": str,
            }
        ],
    }
)

REQ_COLUMNS_SIGNATURES_LIST = [
    "name",
    "position",
    "mail",
]

S_SIGNATURES_LIST = Schema(
    And(
        REQ_COLUMNS_SIGNATURES_LIST
        + [
            "output",
            "phone",
            "phone_country_code",
            "internal_phone",
            "opt_mail",
            "organization_extra",
            "main_font",
            "name_font",
            "max_width",
        ],
        lambda l: (
            len(set(REQ_COLUMNS_SIGNATURES_LIST).intersection(l))
            == len(REQ_COLUMNS_SIGNATURES_LIST)
        ),
    )
)


def is_config(config):
    try:
        S_CONFIG.validate(config)
        return True
    except:
        return False


def is_signatures_list(signatures_list):
    cols = signatures_list[0]
    for i, col in enumerate(cols):
        cols[i] = col.lower().strip()
    try:
        S_SIGNATURES_LIST.validate(cols)
        return True
    except:
        return False
