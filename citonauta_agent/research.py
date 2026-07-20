from __future__ import annotations

import json
import urllib.parse
import urllib.request
from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class ResearchClient:
    timeout_seconds: float = 20.0
    user_agent: str = "CitoNautaAutonomousAgent/0.1"

    def _get_json(self, url: str) -> dict[str, Any]:
        request = urllib.request.Request(
            url,
            headers={"User-Agent": self.user_agent, "Accept": "application/json"},
        )
        with urllib.request.urlopen(request, timeout=self.timeout_seconds) as response:
            return json.loads(response.read().decode("utf-8"))

    @staticmethod
    def _rebuild_abstract(index: dict[str, list[int]] | None) -> str:
        if not index:
            return ""
        positioned: list[tuple[int, str]] = []
        for word, positions in index.items():
            for position in positions:
                positioned.append((int(position), word))
        positioned.sort(key=lambda item: item[0])
        return " ".join(word for _, word in positioned)

    def search_openalex(self, query: str, limit: int) -> list[dict[str, Any]]:
        params = urllib.parse.urlencode(
            {
                "search": query,
                "per-page": limit,
                "select": "id,doi,title,publication_year,authorships,primary_location,abstract_inverted_index,type",
            }
        )
        data = self._get_json(f"https://api.openalex.org/works?{params}")
        results: list[dict[str, Any]] = []
        for work in data.get("results", []):
            title = str(work.get("title") or "").strip()
            if not title:
                continue
            doi = str(work.get("doi") or "").strip()
            url = doi or str(work.get("id") or "").strip()
            authors = []
            for authorship in work.get("authorships", [])[:6]:
                name = str((authorship.get("author") or {}).get("display_name") or "").strip()
                if name:
                    authors.append(name)
            abstract = self._rebuild_abstract(work.get("abstract_inverted_index"))[:1200]
            results.append(
                {
                    "title": title,
                    "url": url,
                    "year": work.get("publication_year"),
                    "type": str(work.get("type") or "artículo académico"),
                    "authors": authors,
                    "abstract_excerpt": abstract,
                }
            )
        return results

    def search_europe_pmc(self, query: str, limit: int) -> list[dict[str, Any]]:
        params = urllib.parse.urlencode(
            {"query": query, "format": "json", "pageSize": limit, "resultType": "core"}
        )
        data = self._get_json(
            f"https://www.ebi.ac.uk/europepmc/webservices/rest/search?{params}"
        )
        results: list[dict[str, Any]] = []
        for item in (data.get("resultList") or {}).get("result", []):
            title = str(item.get("title") or "").strip()
            if not title:
                continue
            doi = str(item.get("doi") or "").strip()
            pmid = str(item.get("pmid") or "").strip()
            pmcid = str(item.get("pmcid") or "").strip()
            if doi:
                url = f"https://doi.org/{doi}"
            elif pmcid:
                url = f"https://europepmc.org/article/PMC/{pmcid}"
            elif pmid:
                url = f"https://europepmc.org/article/MED/{pmid}"
            else:
                continue
            author_text = str(item.get("authorString") or "").strip()
            results.append(
                {
                    "title": title,
                    "url": url,
                    "year": int(item["pubYear"]) if str(item.get("pubYear", "")).isdigit() else None,
                    "type": "literatura biomédica",
                    "authors": [author_text] if author_text else [],
                    "abstract_excerpt": str(item.get("abstractText") or "")[:1200],
                }
            )
        return results

    def collect(
        self,
        title: str,
        description: str,
        limit: int,
        openalex_enabled: bool = True,
        europe_pmc_enabled: bool = True,
    ) -> list[dict[str, Any]]:
        query = f"{title} {description}"[:350]
        combined: list[dict[str, Any]] = []
        if openalex_enabled:
            try:
                combined.extend(self.search_openalex(query, max(3, limit // 2)))
            except Exception as exc:  # network failure must not stop the whole queue
                print(f"[research] OpenAlex no disponible: {exc}")
        if europe_pmc_enabled:
            try:
                combined.extend(self.search_europe_pmc(query, max(3, limit // 2)))
            except Exception as exc:
                print(f"[research] Europe PMC no disponible: {exc}")

        unique: list[dict[str, Any]] = []
        seen: set[str] = set()
        for item in combined:
            marker = str(item.get("url") or item.get("title") or "").casefold()
            if not marker or marker in seen:
                continue
            seen.add(marker)
            unique.append(item)
            if len(unique) >= limit:
                break
        return unique
