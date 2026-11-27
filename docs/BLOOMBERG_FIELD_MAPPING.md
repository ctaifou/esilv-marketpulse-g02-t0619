# Bloomberg Field Mapping

## 1. Objectif et modes autorisés

Ce document définit les règles de correspondance et de normalisation permettant de convertir les données de marché issues de **Bloomberg** vers le **format canonique commun de MarketPulse**, afin que le module `src/analytics.py` puisse les traiter de manière identique aux données Yahoo Finance.

Deux modes d'exécution sont distingués dans l'application :
* **`APPROVED_SAMPLE` (mode par défaut)** : lit le fichier JSON de référence local approuvé (`data/sample/bloomberg_reference_sample.json`). Ce mode est reproductible et permet de tester l'acquisition, le mapping et la normalisation sans disposer d'un Terminal Bloomberg.
* **`LIVE` (environnement autorisé uniquement)** : point d'extension prévu pour interroger un Terminal Bloomberg réel. Ce mode n'est pas actif par défaut et lève une exception `NotImplementedError` tant qu'aucun accès autorisé n'est configuré. Aucune connexion `LIVE` ne doit être simulée.

---

## 2. Identifiants AAPL / SP500

Les identifiants propres à Bloomberg (`provider_identifier`) doivent être traduits vers les tickers canoniques internes utilisés dans MarketPulse (`canonical_ticker`) :

| Ticker MarketPulse | Identifiant Bloomberg (`provider_identifier`) | Instrument |
| :--- | :--- | :--- |
| `AAPL` | `AAPL US Equity` | Apple Inc. (action) |
| `SP500` | `SPX Index` | S&P 500 (indice de référence) |

Dans toutes les observations normalisées produites par le fournisseur, le champ `ticker` doit impérativement contenir **`AAPL`** ou **`SP500`**, et jamais l'identifiant fournisseur Bloomberg.

---

## 3. Correspondance des champs et types

Chaque série du fichier JSON Bloomberg est identifiée par sa clé `provider_identifier` et contient une liste `observations`. Chaque observation brute est convertie vers un dictionnaire Python respectant strictement les 7 clés et types suivants :

| Champ source Bloomberg | Champ cible MarketPulse | Type Python cible | Règle de conversion / format |
| :--- | :--- | :--- | :--- |
| `observation_date` | `date` | `str` | Chaîne au format ISO `AAAA-MM-JJ` |
| `canonical_ticker` (au niveau série) | `ticker` | `str` | Identifiant interne MarketPulse (`AAPL` ou `SP500`) |
| `open_value` | `open` | `float` | Conversion explicite via `float()` |
| `high_value` | `high` | `float` | Conversion explicite via `float()` |
| `low_value` | `low` | `float` | Conversion explicite via `float()` |
| `close_value` | `close` | `float` | Conversion explicite via `float()` |
| `volume_value` | `volume` | `int` | Conversion explicite via `int()` |

---

## 4. Exemple fictif : brut → canonique

> **Note :** Les valeurs ci-dessous sont des données fictives illustrant le contrat de normalisation et ne constituent pas une extraction réelle du marché.

### Donnée brute en entrée (structure JSON Bloomberg)

```json
{
  "provider_identifier": "AAPL US Equity",
  "canonical_ticker": "AAPL",
  "observations": [
    {
      "observation_date": "2026-11-18",
      "open_value": "100.0",
      "high_value": "112.0",
      "low_value": "99.0",
      "close_value": "110.0",
      "volume_value": "1500"
    }
  ]
}