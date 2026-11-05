# Photojournalism-agents

Redaktionel pipeline af konversationelle agenter til en fotojournalistisk arbejdsgang, bygget med Mistral Agents SDK og deployet som managed deployments på Mistral Cloud.

## foto-culler
Vurderer batches JPEG-previews på skarphed, eksponering, komposition, øjeblik og historieværdi i forhold til den opgivne vinkel og returnerer en rangeret shortlist med frame_id, score (0–10) og one-line begrundelse.

## foto-editor
Rådgiver om tonal redigering: anbefaler én darktable-style fra arbejdsgiverens whitelist og et valgfrit crop (højst 15% pr. kant, højst 30% af arealet), verificerer efterfølgende eksporterede JPEG'er mod anbefalingen.

## Udvikling og deploy (pr. agent)

```bash
cd foto-culler   # eller foto-editor
uv run --env-file .env agents chat          # lokal test
uv run --env-file .env agents deploy        # managed deployment på Mistral Cloud
uv run --env-file .env agents chat foto-editor  # chat med den deployede agent
```
