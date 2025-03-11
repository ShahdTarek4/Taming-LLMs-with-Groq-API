import os
import groq
from dotenv import load_dotenv

class LLMClient:
    def __init__(self):
        load_dotenv()  # Load API key from .env file
        self.api_key = os.getenv("GROQ_API_KEY")
        self.client = groq.Client(api_key=self.api_key)
        self.model = "llama-3.3-70b-versatile"  

    def complete(self, prompt, max_tokens=1000, temperature=0.7):
        """Sends a prompt to the model and returns a completion."""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                temperature=temperature
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error: {e}")
            return None

def create_structured_prompt(text, question):
    """Creates a structured prompt that produces a completion with recognizable sections."""
    prompt = f"""
    # Analysis Report

    ## Input Text
    {text}

    ## Question
    {question}

    ## Analysis
    """
    return prompt

def extract_section(completion, section_start, section_end=None):
    """Extracts content between section_start and section_end."""
    start_idx = completion.find(section_start)
    if start_idx == -1:
        return None
    start_idx += len(section_start)

    if section_end is None:
        return completion[start_idx:].strip()

    end_idx = completion.find(section_end, start_idx)
    if end_idx == -1:
        return completion[start_idx:].strip()

    return completion[start_idx:end_idx].strip()

def stream_until_marker(client, prompt, stop_marker, max_tokens=1000):
    """
    Streams the completion and stops once a marker is detected.
    """
    accumulated_text = ""

    try:
        response = client.client.chat.completions.create(
            model=client.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=0.7,
            stream=True  # Enables streaming mode
        )

        for chunk in response:
            if chunk.choices and chunk.choices[0].delta and hasattr(chunk.choices[0].delta, "content"):
                new_text = chunk.choices[0].delta.content
                if new_text:
                    accumulated_text += new_text

                    # Stop streaming when the marker appears
                    if stop_marker in accumulated_text:
                        print(f" Stop marker '{stop_marker}' found. Stopping streaming.")
                        break

    except Exception as e:
        print(f" Streaming Error: {e}")

    return accumulated_text

def classify_with_confidence(text, categories, confidence_threshold=0.8):
    """
    Classifies text into one of the provided categories.
    Returns the classification only if confidence is above threshold.
    """
    # Create a prompt that encourages clear, unambiguous classification
    prompt = f"""
    Classify the following text into exactly one of these categories: {', '.join(categories)}.

    Response format:
    1. CATEGORY: [one of: {', '.join(categories)}]
    2. CONFIDENCE: [high|medium|low]
    3. REASONING: [explanation]

    Text to classify:
    {text}
    """

    # Request completion (without logprobs)
    llm = LLMClient()
    response = llm.client.chat.completions.create(
        model=llm.model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500,
        temperature=0  # Set to 0 for deterministic responses
    )

    # Extract classification details
    completion = response.choices[0].message.content
    category = extract_section(completion, "1. CATEGORY: ", "\n")
    confidence_label = extract_section(completion, "2. CONFIDENCE: ", "\n")

    # Manually estimate confidence based on label
    confidence_mapping = {
        "high": 1.0,
        "medium": 0.5,
        "low": 0.2
    }
    confidence_score = confidence_mapping.get(confidence_label.lower(), 0)

    # Return classification if confidence exceeds threshold
    if confidence_score >= confidence_threshold:
        return {
            "category": category,
            "confidence": confidence_score,
            "reasoning": extract_section(completion, "3. REASONING: ")
        }
    else:
        return {
            "category": "uncertain",
            "confidence": confidence_score,
            "reasoning": "Confidence below threshold"
        }

def compare_prompt_strategies(texts, categories):
    """
    Compares different prompt strategies on the same classification tasks.
    """
    strategies = {
        "basic": lambda text: f"Classify this text into one of these categories: {', '.join(categories)}.\n\nText: {text}",
        "structured": lambda text: f"""
        Classification Task
        Categories: {', '.join(categories)}
        Text: {text}
        Classification: """,
        "few_shot": lambda text: f"""
        Here are some examples of text classification:
        Example 1:
        Text: "The product arrived damaged and customer service was unhelpful."
        Classification: Negative
        Example 2:
        Text: "While delivery was slow, the quality exceeded my expectations."
        Classification: Mixed
        Example 3:
        Text: "Absolutely love this! Best purchase I've made all year."
        Classification: Positive
        Now classify:
        {text}
        """
    }

    results = {}

    for strategy_name, prompt_func in strategies.items():
        strategy_results = []
        for text in texts:
            prompt = prompt_func(text)
            result = classify_with_confidence(text, categories)
            strategy_results.append(result)
        results[strategy_name] = strategy_results

    return results


'''//part 1 testing
if __name__ == "__main__":
    llm = LLMClient()
    response = llm.complete("What is AI?")
    print("Basic Completion Output:")
    print(response)

//part 2 testing
if __name__ == "__main__":
    llm = LLMClient()
    
    text = "Artificial intelligence has increased job opportunities."
    question = "What are the major impacts of AI on jobs?"

    structured_prompt = create_structured_prompt(text, question)
    response = llm.complete(structured_prompt)
    extracted_analysis = extract_section(response, "## Analysis")

    print("\n  Full Structured Completion Output:")
    print(response)

    print("\n Extracted 'Analysis' Section:")
    print(extracted_analysis)

    # Stop Marker Test
    stop_marker = "### End"
    structured_prompt_with_marker = structured_prompt + "\n" + stop_marker
    streamed_response = stream_until_marker(structured_prompt_with_marker, stop_marker)

    print("\n Streamed Response (Stopped at Marker):")
    print(streamed_response)


//part 3 testing
if __name__ == "__main__":
    categories = ["Positive", "Negative", "Mixed"]
    text = "Athelte's earn a lot, however, their risk of injury is extremely high."

    result = classify_with_confidence(text, categories)
    print("Classification with Confidence Output:")
    print(result)'''
'''//part 4 testing
if __name__ == "__main__":
    texts = ["The phone is very fast and smooth, but the camera quality is disappointing.", "Absolutely loved this movie!", "This was a complete waste of money."]
    categories = ["Positive", "Negative", "Mixed"]
    
    comparison = compare_prompt_strategies(texts, categories)
    print(comparison)'''




