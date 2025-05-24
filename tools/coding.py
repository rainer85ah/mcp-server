from agents.coding import coding_agent


@coding_agent.tool()
def generate_code(prompt: str, language: str = "python") -> str:
    """Generate boilerplate code in a given language based on the prompt."""
    if language.lower() == "python":
        return f"# Python code for: {prompt}\n\n" \
               f"def main():\n    # TODO: Implement\n    pass\n\nif __name__ == '__main__':\n    main()"
    elif language.lower() == "javascript":
        return f"// JavaScript code for: {prompt}\n\n" \
               f"function main() {{\n    // TODO: Implement\n}}\n\nmain();"
    else:
        return f"// Code for: {prompt} in {language}\n\n// TODO: Not implemented for this language yet."
