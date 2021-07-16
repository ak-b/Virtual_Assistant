def get_iprep():
    card = {
    "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
    "type": "AdaptiveCard",
    "version": "1.1",
    "body": [
        {
            "type": "ColumnSet",
            "columns": [
                {
                    "type": "Column",
                    "width": 2,
                    "items": [
                        {
                            "type": "TextBlock",
                            "text": "Search for IP Reputation",
                            "weight": "Bolder",
                            "size": "Medium",
                            "wrap": True,
                            "id": "function"
                        },
                        {
                            "type": "TextBlock",
                            "text": "This function allow you to search the threat level for an IP",
                            "isSubtle": True,
                            "wrap": True
                        },
                        {
                            "type": "Container",
                            "items": [
                                {
                                    "type": "TextBlock",
                                    "text": "IP Reputation DB",
                                    "wrap": True
                                },
                                {
                                    "type": "Input.Text",
                                    "id": "search_iprep_ip",
                                    "placeholder": "Please input IP address"
                                }
                            ]
                        },
                        {
                            "type": "Container",
                            "items": [
                                {
                                    "type": "TextBlock",
                                    "text": "IP Reputation Search",
                                    "wrap": True
                                },
                                {
                                    "type": "Input.Text",
                                    "id": "show_iprep",
                                    "placeholder": "please input a device interface"
                                }
                            ]
                        }
                    ]
                },
                {
                    "type": "Column",
                    "width": 1,
                    "items": [
                        {
                            "type": "Image",
                            "url": "https://i.ytimg.com/vi/uzum7GpHhTQ/hqdefault.jpg",
                            "size": "auto"
                        }
                    ]
                }
            ]
        }
    ],
    "actions": [
        {
            "type": "Action.Submit",
            "title": "Submit"
        }
    ]
}
    return card

