# NeoChef: Project Concept & Roadmap

## Vision & Positioning

**Name:** NeoChef\
**Subtitle:** "A local recipe graph: discover meals from what you
already have."

**Elevator Pitch:**\
NeoChef builds a recipe--ingredient graph and computes ingredient
similarity to quickly find dishes from your fridge and suggest
alternatives. Everything runs locally: Neo4j, Python, LangChain, no
LLMs, no external servers.

------------------------------------------------------------------------

## Goals and Non-Goals

**Core Goals:** 1. Import 2--5k recipes from an open source/API/CSV with
local cache.\
2. Graph model with `Recipe`, `Ingredient`, `USES`, `SIMILAR_TO`.\
3. Automated ETL pipeline with LangChain (no LLMs): fetch → normalize →
compute similarities → load.\
4. Streamlit UI with three main scenarios:\
- Find recipes by ingredients.\
- Explore ingredient substitutions.\
- Graph visualization for recipes/ingredients.\
5. Export shopping list for selected recipe.

**Non-Goals:** - Advanced nutrition or diets.\
- Machine learning recommender systems.\
- Public deployment as a hosted service.

------------------------------------------------------------------------

## Key User Scenarios

1.  **Pantry Picker:** select available ingredients → get matching
    recipes.\
2.  **Ingredient Swaps:** click on an ingredient → see alternatives
    based on co-occurrence.\
3.  **Recipe Explorer:** open a recipe → view its ingredients, similar
    ones, and related recipes as a subgraph.\
4.  **Shopping List:** export missing ingredients into a shopping list.

------------------------------------------------------------------------

## Architecture

    [Source (CSV/API)] → [LangChain ETL Pipeline]
         Extract → Normalize → Similarities → Load Neo4j
                                         |
                                   [local cache (Parquet/JSON)]
                                            |
                                      [Streamlit UI]
                                 (queries Cypher via neo4j-driver)

-   **Storage:** Neo4j (Desktop or Aura Free).\
-   **Orchestration:** LangChain (Runnables/Chains/Tools, no LLM).\
-   **UI:** Streamlit (no CLI).\
-   **Cache:** Local Parquet/JSON in `data/`.

------------------------------------------------------------------------

## Data Model

**Nodes** -
`:Recipe {id, title, url, image, cuisine, source, timeMinutes, instructionsText}`\
- `:Ingredient {id, name, normalizedName}`\
- `:Tag {name}` (optional, e.g. vegan, spicy)

**Relationships** - `(:Recipe)-[:USES {qty, unit}]->(:Ingredient)`\
- `(:Ingredient)-[:SIMILAR_TO {score}]->(:Ingredient)`\
- `(:Recipe)-[:HAS_TAG]->(:Tag)` (optional)

**Indexes** - `(:Recipe id)` and `(:Ingredient normalizedName)`

------------------------------------------------------------------------

## Algorithms

-   **Ingredient normalization:** lowercasing, trimming, removing units
    in parentheses, lemmatization of plurals, synonym dictionary
    (`chili pepper` → `chili`, `scallion` → `green onion`).\
-   **Co-occurrence score:**
    -   Jaccard: `|R(i) ∩ R(j)| / |R(i) ∪ R(j)|`\
    -   Alternative: PMI-lite `cooc / sqrt(freq(i)*freq(j))`\
    -   Keep top-k neighbors and threshold.

------------------------------------------------------------------------

## LangChain ETL Pipeline

**Components:** - `FetchRecipesTool`: load from API/CSV.\
- `NormalizeIngredientsRunnable`: normalize ingredient names.\
- `BuildInvertedIndexRunnable`: map ingredients to recipe sets.\
- `ComputeSimilaritiesRunnable`: compute similarity scores.\
- `Neo4jWriterTool`: batch MERGE nodes/edges.\
- `ReportRunnable`: generate coverage statistics.

**Sequence:**\
`Fetch → Normalize → BuildIndex → ComputeSimilarities → WriteNeo4j → Report`

------------------------------------------------------------------------

## Streamlit UI

1.  **Pantry Picker:** multi-select ingredients, see recipe cards with
    missing items.\
2.  **Ingredient Explorer:** search ingredient, see similar ones and top
    recipes.\
3.  **Recipe Graph View:** visualize subgraph (using pyvis/networkx from
    Neo4j).\
4.  **Data Refresh:** trigger LangChain ETL pipeline.

------------------------------------------------------------------------

## Roadmap

**Week 1:**\
- Setup Neo4j + repo structure.\
- Fetch sample recipes and cache.\
- Implement normalization and basic ingestion.\
- Create similarity edges.\
- Write Cypher queries for key scenarios.

**Week 2:**\
- Build Streamlit UI (Pantry Picker, Ingredient Explorer).\
- Add recipe graph visualization.\
- Implement shopping list export.\
- Polish UX, add metrics (coverage, density).

------------------------------------------------------------------------

## Metrics of Success

-   Unique ingredients and recipes imported.\
-   Average degree of `Ingredient` nodes.\
-   Quality of `SIMILAR_TO` edges (average score).\
-   Response time for queries in UI.

------------------------------------------------------------------------

## Future Extensions

-   Seasonality of ingredients.\
-   Tags for diets.\
-   Cost estimation from price CSV.\
-   Multi-source ingestion with deduplication.

------------------------------------------------------------------------