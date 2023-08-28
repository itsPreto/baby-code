from mitmproxy import http
import re


def response(flow: http.HTTPFlow) -> None:
    if flow.request.pretty_url == "http://127.0.0.1:8080":  # the url of the AI model server
        # this is a response from the AI model server
        data = flow.response.text  # get the response data
        # check if the response contains Python code and store it if it does
        codeBlockRegex = r'```python\n([\s\S]*?)```'
        matches = re.findall(codeBlockRegex, data)
        if matches:
            for match in matches:
                print(f"Found Python code in response: {match}")  # replace this with your actual code storage function
