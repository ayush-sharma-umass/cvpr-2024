from dash import html, dcc

def create_instruction_box(text_main: str, text_body: str, include_arrow: bool = False):
    """
    Create an instruction box with a title, body text and optional arrow (arrow is disabled for now)
    :param text_main: Title text
    :param text_body: Body text
    :param include_arrow: Include an arrow at the bottom of the box
    TODO: Make it markdown compatible
    """
    arrow_style = {
        'position': 'relative',
        'marginTop': '20px',  # Add margin to ensure space between text and arrow
        'width': '50px',  # Adjust the width as needed
        'height': '50px'  # Maintain aspect ratio or set fixed height
    }

    children = [
        html.Div(
            children=text_main,
            style={
                'font-family': 'Balto',
                'fontSize': '24px',
                'fontWeight': 'bold',
                'textAlign': 'center',
                'marginBottom': '20px'
            }
        ),
        html.Div(
            children=text_body,
            style={
                'font-family': 'Courier New',
                'fontSize': '18px',
                'textAlign': 'left',
                'position': 'relative'  # To ensure arrow is relative to text_body
            }
        )
    ]

    # if include_arrow:
    #     children.append(
    #         html.Img(
    #             src='/assets/kisspng-pencil-arrow-computer-icons-left-arrow-5ad71977ab9987.0525584315240461997029.png',
    #             style=arrow_style
    #         )
    #     )

    return html.Div(
        style={
            'backgroundColor': '#93E9BE',
            'paddingTop': '30px',  # Top padding
            'paddingBottom': '50px',  # Bottom padding
            'paddingLeft': '40px',  # Left padding
            'paddingRight': '40px',  # Right padding
            'border': '2px solid white',
            'borderRadius': '10px',
            'display': 'flex',
            'flexDirection': 'column',
            'alignItems': 'center',
            'justifyContent': 'center',
            'width': '50%',
            'margin': 'auto',
            'position': 'relative',  # To position the arrow correctly
            'marginBottom': '20px'  # Add bottom margin for vertical spacing
        },
        children=children
    )


def create_radio_buttons(uid: str, options: list[str], selected: str, header: str):
    """
    Create a radio button with a header and options
    :param options: List of options
    :param selected: Default selected option
    :param header: Header text
    """
    return html.Div(
        children=[
            html.H3(header, style={'textAlign': 'center', 'marginBottom': '20px'}),
            html.Div(
                children=[
                    dcc.RadioItems(
                        id=uid,
                        options=[{'label': option, 'value': option} for option in options],
                        value=selected,
                        labelStyle={
                            'display': 'block',
                            'padding': '10px 10px 10px 0',  # Add padding on top, right, bottom and left
                        },
                        style={
                            'marginBottom': '10px'  # Space between the options and box bottom
                        }
                    )
                ],
                style={
                    'backgroundColor': '#FFFFE0',  # Light yellow color
                    'border': '1px solid #ccc',
                    'borderRadius': '5px',
                    'padding': '10px',  # Padding inside the box
                    'width': '300px',  # Width of the box
                    'margin': 'auto',  # Center the box
                    'font-family': 'Helvetica' #  font family
                }
            )
        ],
        style={
            'padding': '20px'  # Padding around the whole container
        }
    )


def create_explanation_box(markdown_text: str):
    """
    Create an explanation box with markdown text
    :param uid: Unique ID for the box
    :param markdown_text: Markdown text to display
    """
    return html.Div(
        children=[
            dcc.Markdown(
                markdown_text,
                style={
                    'fontSize': '16px',
                    'textAlign': 'justify',
                }
            )
        ],
        style={
            'backgroundColor': '#FFF9C4',  # Light yellow color
            'border': '1px solid #ccc',
            'borderRadius': '5px',
            'padding': '20px',  # Padding inside the box
            'width': '80%',  # Width of the box
            'margin': '20px auto'  # Center the box with some vertical margin
        }
    )
