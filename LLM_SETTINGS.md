# LLM feature configuration

Plainews provides a number of smart features that make reading news faster and easier. These are:
* Article summarization
* Translations

For them to work, an LLM connection must be established. This is done in the plainews configuration. General information about the configuration format and parameters you will find in the [README.md](README.md). Here, we will focus on the LLM-related parameters from there.

The default LLM section of the config is:

```yaml
llm_model: ollama/llama3.1
llm_base_url: http://localhost:11434
language: english
```

Plainews uses the [LiteLLM library](https://docs.litellm.ai/docs/) to unify for interface between different LLMs. This should already give you an idea how an LLM is configured in Plainews.

## LLM model (`llm_model`)

The model to use for smart features. The list of available models can be found LiteLLM's documentation [here](https://docs.litellm.ai/docs/providers). From there you need the name of the model that you see in the examples.
For instance, if you want to use OpenAI, you will see on its page [here](https://docs.litellm.ai/docs/providers/openai) that one model you can use is the "gpt-4o".
In the default config, Ollama is configured using the Llama 3.1 model.

## LLM base URL (`llm_base_url`)

Most LLMs will not require this. Ones that run locally on your computer, though, would. In the default example, where Ollama is used, the URL of the locally running Ollama server needs to be specified. 

## Language (`language`)

If you want to use an LLM in order to translate articles, the language property can be used to specify the target language. Here, a human readable version of the language is enough - you don't have to use some two or three letter language code. The value is used as part of the prompt and LLMs are typically smart enough to understand what you mean. You can even play around and give more than just the language. You could instruct the LLM to use English, but with words that a baby would use.   
