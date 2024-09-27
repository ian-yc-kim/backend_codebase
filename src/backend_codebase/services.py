import openai

openai.api_key = "YOUR_API_KEY"

def generate_chapter_content(title, previous_content, user_prompts):
    prompt = f"Title: {title}\nPrevious Content: {previous_content}\nUser Prompts: {user_prompts}\nGenerate the next chapter content:"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.7,
    )
    return response.choices[0].text.strip()
