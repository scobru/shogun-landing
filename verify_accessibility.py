from html.parser import HTMLParser
import sys

class AccessibilityVerifier(HTMLParser):
    def __init__(self):
        super().__init__()
        self.found_theme_toggle = False
        self.theme_toggle_has_aria_label = False
        self.found_tooltip_wrapper = False
        self.tooltip_has_data_tip = False
        self.tooltip_has_class = False

    def handle_starttag(self, tag, attrs):
        attr_dict = dict(attrs)

        # Check for tooltip wrapper
        if tag == 'div' and 'id' in attr_dict and attr_dict['id'] == 'theme-tooltip':
            self.found_tooltip_wrapper = True
            if 'data-tip' in attr_dict:
                self.tooltip_has_data_tip = True
            if 'tooltip' in attr_dict.get('class', '').split():
                self.tooltip_has_class = True

        # Check for theme toggle button
        if tag == 'button' and 'id' in attr_dict and attr_dict['id'] == 'theme-toggle':
            self.found_theme_toggle = True
            if 'aria-label' in attr_dict:
                self.theme_toggle_has_aria_label = True

def verify():
    parser = AccessibilityVerifier()
    try:
        with open('index.html', 'r') as f:
            parser.feed(f.read())
    except FileNotFoundError:
        print("FAIL: index.html not found")
        sys.exit(1)

    print(f"Found theme toggle button: {parser.found_theme_toggle}")
    print(f"Theme toggle has aria-label: {parser.theme_toggle_has_aria_label}")
    print(f"Found tooltip wrapper: {parser.found_tooltip_wrapper}")
    print(f"Tooltip wrapper has data-tip: {parser.tooltip_has_data_tip}")
    print(f"Tooltip wrapper has class 'tooltip': {parser.tooltip_has_class}")

    if (parser.found_theme_toggle and
        parser.theme_toggle_has_aria_label and
        parser.found_tooltip_wrapper and
        parser.tooltip_has_data_tip and
        parser.tooltip_has_class):
        print("PASS: Theme toggle is accessible and has tooltip")
    else:
        print("FAIL: Theme toggle is not accessible or missing tooltip")
        sys.exit(1)

if __name__ == "__main__":
    verify()
