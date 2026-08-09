# AI stills

Prompts: `prompts.json`

Generate / regenerate with OpenAI credits:

```bash
python scripts/youtube/images_openai.py 03
```

If generation fails (quota), slideshow render falls back to `pipeline.png` / `metrics-callout.png`.
Current `*.png` files may be temporary placeholders until OpenAI credits are available.
