
def completion_to_prompt(completion):
    return f"\n</s>\n\n{completion}</s>\n\n"

def messages_to_prompt(messages):
    prompt = ""
    for message in messages:
        prompt += f"\n{message.content}</s>\n"

    if not prompt.startswith("\n"):
        prompt = "\n</s>\n" + prompt

    prompt = prompt + "\n"
    return prompt