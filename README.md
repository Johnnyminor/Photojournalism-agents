# Photojournalism-agents

Redaktionel pipeline af konversationelle agenter til en fotojournalistisk arbejdsgang, bygget med Mistral Agents SDK og deployet som managed deployments på Mistral Cloud.

## foto-culler
Vurderer batches JPEG-previews på skarphed, eksponering, komposition, øjeblik og historieværdi i forhold til den opgivne vinkel og returnerer en rangeret shortlist med frame_id, score (0–10) og one-line begrundelse.

## foto-editor
Rådgiver om tonal redigering: anbefaler én darktable-style fra arbejdsgiverens whitelist og et valgfrit crop (højst 15% pr. kant, højst 30% af arealet), verificerer efterfølgende eksporterede JPEG'er mod anbefalingen.

## Udvikling og deploy (pr. agent)

```bash
cd foto-culler   # eller foto-editor / foto-captioner
uv run --env-file ../.env agents serve      # self-hosted worker (kræver ingen deployment-slot)
uv run --env-file ../.env agents chat       # lokal test
uv run --env-file ../.env agents deploy     # managed deployment (kræver abonnement)
```

## Billedupload til en servet agent

Vibe-chatsiden understøtter ikke vedhæftninger. Brug `send_images.py` fra repo-roden,
mens `agents serve` kører i en anden terminal:

```bash
uv run --project foto-culler --env-file .env python send_images.py foto-culler \
  "/home/bruger/Pictures/RAW billeder/"*.jpg -m "Vinkel: ..."
```

Modellen accepterer kun JPEG, PNG, WEBP, GIF, MPO, HEIF, AVIF, BMP og TIFF — ikke RAW (.CR2/.NEF).
Eksportér 1600 px JPEG-previews først (f.eks. via darktable) og peg på dem.

## foto-captioner
Skriver billedtekster efter pressetik ud fra synlig information og bekræftede fakta: hvad der ses, hvem, hvornår og hvor. Uafklarte fakta markeres eksplicit — aldrig gæt. Output pr. billede: frame_id, billedtekst, credit-linje og keywords (ens across serien).
