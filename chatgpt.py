import os
import openai
openai.api_key = "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"

def nlp(msg):
  try:
    completion = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[
        {"role": "user", "content": msg}
      ]
    )
  except openai.error.RateLimitError as e:
    return "That model is currently overloaded with other requests. You can retry your request, or contact us through our help center at help.openai.com if the error persists."

  return completion.choices[0].message['content']

