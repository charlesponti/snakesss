candidate_schema = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "name": {"type": "string", "description": "Name of the agency"},
            "agencyBio": {
                "type": "string",
                "description": "Biography or description of the agency",
            },
            "position": {
                "type": "string",
                "description": "Position or role of the agency",
            },
            "tags": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "label": {
                            "type": "string",
                            "description": "Label or name of the tag",
                        },
                    },
                },
                "description": "List of tags associated with the agency",
            },
            "representatives": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "Name of the representative",
                        },
                        "organization": {
                            "type": "string",
                            "description": "Organization the representative belongs to",
                        },
                        "representationType": {
                            "type": "string",
                            "description": "Type of representation",
                        },
                        "phoneNumbers": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "number": {
                                        "type": "string",
                                        "description": "Phone number",
                                    },
                                    "contactType": {
                                        "type": "string",
                                        "description": "Type of contact (e.g., work, mobile)",
                                    },
                                },
                            },
                            "description": "List of phone numbers for the representative",
                        },
                        "emails": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "address": {
                                        "type": "string",
                                        "description": "Email address",
                                    },
                                    "contactType": {
                                        "type": "string",
                                        "description": "Type of contact (e.g., work, personal)",
                                    },
                                },
                            },
                            "description": "List of email addresses for the representative",
                        },
                    },
                },
                "description": "List of representatives associated with the agency",
            },
            "phoneNumbers": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "number": {"type": "string", "description": "Phone number"},
                        "contactType": {
                            "type": "string",
                            "description": "Type of contact (e.g., work, mobile)",
                        },
                    },
                },
                "description": "List of phone numbers for the agency",
            },
            "emails": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "address": {"type": "string", "description": "Email address"},
                        "contactType": {
                            "type": "string",
                            "description": "Type of contact (e.g., work, personal)",
                        },
                    },
                },
                "description": "List of email addresses for the agency",
            },
        },
    },
}
