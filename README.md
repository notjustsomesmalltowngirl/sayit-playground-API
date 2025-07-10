# chat Playground API
A fun and simple API that returns interactive game prompts like **"Would You Rather"** , **"Never Have I Ever"**, **Riddles**, **Hypotheticals**, and more — perfect for chat apps, games, or boredom busters!

## ✨ Features
- Returns fun prompts in JSON format

- Games include:
  
  - Did You Know
  
  - Hypotheticals
  
  - Hot Takes
  
  - Never Have I Ever
  
  - Would You Rather
  
  - Story Builder
  
  - Riddles
  
  - Two Truths and a Lie

## Example Response 

```
{
  "category": "pop_culture",
  "opinion": "Remakes rarely improve on the original."
}
```

## Available Endpoints
| Endpoint           | Description                                                        |
| ------------------ | ------------------------------------------------------------------ |
| `/api/v1/all-game-types`       | Returns a list of all available game types                             |
| `/api/v1/get-random?game_type=...` | Returns a single random game from the type specified in the query  |
|`/api/v1/get-by-type?game_type=...` | Returns a list of games of the specified type                      |

## Game Types You Can Query

- did-you-know

- hypotheticals

- hot-takes

- never-have-i-ever

- would-you-rather

- story-builder

- riddles

- two-truths-and-a-lie

## Deployment
This API is live at:
https://sayit-playground-api.onrender.com

## Made With ❤️
Built by [**Happiness**]([https://your-link.com](https://github.com/uptowngirl757)) and [**Peace Dara**]([https://sisters-link.com](https://github.com/notjustsomesmalltowngirl)) — two curious minds who love mixing code with creativity.


