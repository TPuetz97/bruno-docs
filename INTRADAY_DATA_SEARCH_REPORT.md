# 🔍 S&P 500 Intraday-Daten Suche (1990-2026)

**Suchdatum:** 22. Oktober 2026  
**Ziel:** Intraday-Daten (Stunden-/Minutendaten) für den S&P 500 von 1990 bis 2026 finden

---

## ⚠️ **Hauptergebnis: NICHT VERFÜGBAR über kostenlose APIs**

**Historische Intraday-Daten bis 1990 sind über kostenlose Datenquellen wie Yahoo Finance NICHT verfügbar.**

---

## 📊 Was ist verfügbar?

### ✅ **Verfügbare Intraday-Daten**

| Datenquelle | Zeitraum | Intervalle | Anzahl Datenpunkte |
|-------------|----------|------------|-------------------|
| **Yahoo Finance** | Letzten **~2 Jahre** | 1m, 5m, 15m, 30m, 1h | Bis zu 3,479 Kerzen |
| ^GSPC (S&P 500 Index) | 22.10.2024 - 22.10.2026 | 1 Stunde | 3,479 |
| SPY (S&P 500 ETF) | 22.10.2024 - 22.10.2026 | 1 Stunde | 3,478 |
| ES=F (E-mini Futures) | 22.10.2024 - 22.10.2026 | 1 Stunde | 11,429 * |

*E-mini Futures haben mehr Datenpunkte, da sie 24h handeln (keine regulären Handelszeiten)

### 📋 **Detaillierte Verfügbarkeit nach Intervall**

| Intervall | Maximaler Zeitraum | Datenpunkte | Status |
|-----------|-------------------|-------------|---------|
| **1 Minute** | 5 Tage | 1,826 | ✅ Verfügbar |
| **5 Minuten** | 30 Tage | 1,717 | ✅ Verfügbar |
| **15 Minuten** | 60 Tage | Nicht getestet | ⚠️ Begrenzt |
| **30 Minuten** | 60 Tage | Nicht getestet | ⚠️ Begrenzt |
| **1 Stunde** | **730 Tage (2 Jahre)** | 3,479 | ✅ Maximum |

---

## ❌ Was ist NICHT verfügbar?

### **Getestete historische Zeiträume (ALLE negativ):**

| Jahr | Verfügbarkeit | Getestetes Intervall |
|------|---------------|---------------------|
| 1990 | ❌ Nicht verfügbar | 1 Stunde |
| 1995 | ❌ Nicht verfügbar | 1 Stunde |
| 2000 | ❌ Nicht verfügbar | 1 Stunde |
| 2010 | ❌ Nicht verfügbar | 1 Stunde |
| 2015 | ❌ Nicht verfügbar | 1 Stunde |
| 2020 | ❌ Nicht verfügbar | 1 Stunde |
| 2023 | ❌ Nicht verfügbar | 1 Stunde |
| 2024 (ganz) | ❌ Nicht verfügbar | 1 Stunde |

**Alle Anfragen für historische Jahre vor Oktober 2024 wurden von Yahoo Finance abgelehnt.**

---

## 🔒 **Warum sind historische Intraday-Daten nicht verfügbar?**

### 1. **API-Limitierungen**

Yahoo Finance und andere kostenlose APIs haben strikte Limits:

```
Fehlermeldung von Yahoo Finance API:
"1h data not available for startTime=631170000 and endTime=662619600. 
The requested range must be within the last 730 days."
```

**Klare Grenze:** Nur die letzten **730 Tage** (2 Jahre) sind verfügbar.

### 2. **Datenspeicherung und Kosten**

- Intraday-Daten sind **voluminös**: 1 Jahr Minutendaten = Millionen von Datenpunkten
- **Speicherkosten** sind hoch
- **Bandbreite** für kostenlose APIs ist begrenzt
- Kostenlose Anbieter priorisieren tägliche Daten über Intraday

### 3. **Kommerzielle Interessen**

- Historische Intraday-Daten haben **hohen kommerziellen Wert**
- Professionelle Trader und Hedge Funds zahlen dafür
- Datenanbieter verkaufen diese Daten separat

### 4. **Historische Datenerfassung**

- Minuten-/Stundendaten wurden in den 1990er Jahren **nicht systematisch gespeichert**
- Elektronischer Handel war weniger verbreitet
- Datenerfassung begann erst später im großen Stil

---

## 💰 **Alternative Datenquellen (Kommerzielle Anbieter)**

Wenn Sie historische Intraday-Daten bis 1990 benötigen, gibt es folgende **kostenpflichtige** Optionen:

### 🏦 **1. Professionelle Finanzdatenanbieter**

| Anbieter | Verfügbarkeit | Kosten | Zugang |
|----------|---------------|--------|--------|
| **Bloomberg Terminal** | Intraday ab ~1990er | $24,000+/Jahr | Professionell |
| **Refinitiv (Reuters)** | Umfangreiche Historie | $15,000+/Jahr | Institutionell |
| **FactSet** | Tick-Level Daten | $10,000+/Jahr | Professionell |
| **S&P Capital IQ** | S&P eigene Daten | Preis auf Anfrage | Institutionell |

**Vorteile:** Höchste Qualität, vollständige Historie, Support  
**Nachteile:** Sehr teuer, meist nur für Institutionen

### 📈 **2. Spezialisierte Marktdaten-APIs**

| Anbieter | Verfügbarkeit | Kosten | API |
|----------|---------------|--------|-----|
| **Polygon.io** | Minutendaten ab 2004 | $99-$999/Monat | REST/WebSocket |
| **Alpha Vantage** | Intraday begrenzt | $49-$499/Monat | REST |
| **Quandl (Nasdaq Data Link)** | Verschiedene Datasets | $50-$500/Monat | API |
| **IEX Cloud** | Intraday ab ~2015 | $9-$499/Monat | REST |
| **Tiingo** | Intraday ab ~2015 | $10-$125/Monat | REST |

**Vorteile:** Günstiger, API-Zugang, flexibel  
**Nachteile:** Historie oft nur bis ~2004-2015, nicht zurück bis 1990

### 🎓 **3. Akademische Datenbanken**

| Datenbank | Verfügbarkeit | Zugang | Kosten |
|-----------|---------------|--------|--------|
| **CRSP (Wharton)** | Intraday ab ~1993 (TAQ) | Universitäten | Akademisch/Teuer |
| **Compustat** | Tick-Level möglich | Institutionell | Lizenz erforderlich |
| **TAQ Database** | Trade & Quote seit 1993 | NYSE/Nasdaq | Sehr teuer |
| **WRDS** | Verschiedene Quellen | Universitäten | Institutioneller Zugang |

**Vorteile:** Höchste Qualität für Forschung  
**Nachteile:** Zugang oft nur über Universitäten, sehr teuer

### 🚀 **4. Quant-Plattformen**

| Plattform | Verfügbarkeit | Kosten | Features |
|-----------|---------------|--------|----------|
| **QuantConnect** | Minutendaten ab 1998 | Kostenlos-$300/Monat | Backtesting-Plattform |
| **Quantopian (archiviert)** | War kostenlos | Nicht mehr aktiv | - |
| **Alpaca Markets** | Begrenzte Historie | Kostenlos (Trading) | Broker + Daten |
| **Interactive Brokers** | Historische Daten | Broker-Account | Trading-Plattform |

**Vorteile:** Oft günstiger, integriert mit Backtesting  
**Nachteile:** Historie variiert, nicht immer bis 1990

---

## 🎯 **Realistische Erwartungen**

### Was Sie erwarten können:

| Zeitraum | Intraday-Verfügbarkeit | Empfohlene Quelle |
|----------|------------------------|-------------------|
| **2024-2026** | ✅ **Stündlich verfügbar** | Yahoo Finance (kostenlos) |
| **2020-2024** | ⚠️ Möglich mit Einschränkungen | Polygon.io, IEX Cloud |
| **2010-2020** | ⚠️ Begrenzt verfügbar | Polygon.io, QuantConnect |
| **2000-2010** | ❌ Schwer zu bekommen | Bloomberg, CRSP |
| **1990-2000** | ❌ **Sehr schwer/unmöglich** | Bloomberg Terminal, CRSP |

### **Warum ist 1990-2000 so schwierig?**

1. **Elektronischer Handel** war nicht so verbreitet
2. **Datenerfassung** war nicht standardisiert
3. **Speicherung** von Minutendaten war teuer/unpraktisch
4. **Verfügbare Daten** wurden oft nicht langfristig archiviert

---

## 💡 **Empfehlungen basierend auf Ihrem Use Case**

### **Option 1: Nutzen Sie tägliche OHLC-Daten (1990-2026) ✅**

**Vorteile:**
- ✅ Vollständig verfügbar von 1990 bis heute
- ✅ Kostenlos über Yahoo Finance
- ✅ 9,268 Handelstage analysiert
- ✅ Statistisch signifikante Ergebnisse

**Für Ihre ursprüngliche Frage bereits durchgeführt:**
- Opening vs. Previous Close: ✅ Beantwortet (31.52% höher)
- Jahrzehnt-Analyse: ✅ Komplett
- Wochentags-Muster: ✅ Umfassend

**Einschränkung:**
- ❌ Keine präzisen Intraday-Zeitpunkte (z.B. "1 Stunde nach Opening")

---

### **Option 2: Intraday-Analyse nur für letzte 2 Jahre (2024-2026)**

**Was bereits gemacht wurde:**
- ✅ 501 Handelstage mit Stundendaten analysiert
- ✅ Erste Stunde nach Opening: +$0.85 Durchschnitt (53.09% positiv)
- ✅ Letzte Stunde vor Closing: -$0.22 Durchschnitt (ausgeglichen)

**Verfügbare Intervalle:**
- 1-Minuten-Daten: Letzte 5 Tage
- 5-Minuten-Daten: Letzten Monat
- Stundendaten: Letzte 2 Jahre

---

### **Option 3: Approximation mit täglichen High/Low-Daten**

**Bereits implementiert in der Hauptanalyse:**

```
Durchschnittliche Tagesspanne: $22.61
Durchschnitt Open → High: +$10.93
Durchschnitt Open → Low: -$11.68
```

**Dies gibt Ihnen:**
- ✅ Intraday-Bewegungsrichtung (grob)
- ✅ Volatilität innerhalb des Tages
- ✅ Verfügbar für alle 9,268 Handelstage

**Einschränkung:**
- ❌ Kein exakter Zeitpunkt, nur High/Low des Tages

---

### **Option 4: Investieren Sie in kommerzielle Daten**

**Wenn Sie wirklich Intraday-Daten bis 1990 brauchen:**

**Budget < $100/Monat:**
- → **Polygon.io** (ab 2004, $99/Monat)
- → **QuantConnect** (ab 1998, Minutendaten)

**Budget $100-500/Monat:**
- → **Alpha Vantage Premium**
- → **Quandl Premium**

**Budget $500+/Monat:**
- → **Bloomberg Terminal** (beste Qualität)
- → **Refinitiv**

**Akademischer Zugang:**
- → Prüfen Sie, ob Ihre Universität **WRDS** oder **CRSP** hat

---

## 📝 **Zusammenfassung der durchgeführten Tests**

### Getestete Kombinationen: **24**

| Test-Typ | Anzahl | Erfolge | Misserfolge |
|----------|--------|---------|-------------|
| yfinance Intervall/Periode | 12 | 6 | 6 |
| Historische Jahres-Anfragen | 8 | 0 | 8 |
| Alternative Symbole | 4 | 4 | 0 |

### **Erfolgreiche Abfragen:**

1. ✅ 1-Minute Daten: 5 Tage zurück
2. ✅ 5-Minuten Daten: 30 Tage zurück
3. ✅ 1-Stunden Daten: **730 Tage zurück (Maximum!)**
4. ✅ Alle S&P 500 Symbole (^GSPC, SPY, ^SPX, ES=F)

### **Fehlgeschlagene Abfragen:**

1. ❌ Alle Anfragen für Jahre vor Oktober 2024
2. ❌ 1-Minute/5-Minute Daten über 60 Tage hinaus
3. ❌ Stundendaten für mehr als 2 Jahre

---

## 🔬 **Technische Details**

### API-Limits von Yahoo Finance:

```
- 1-Minute Daten: Max. 8 Tage
- 5-Minuten Daten: Max. 60 Tage  
- 15-Minuten Daten: Max. 60 Tage
- 30-Minuten Daten: Max. 60 Tage
- 1-Stunden Daten: Max. 730 Tage (2 Jahre)
- 1-Tages Daten: Unbegrenzt (zurück bis ~1927)
```

### Getestete Symbole:

1. **^GSPC** - S&P 500 Index (offiziell)
2. **SPY** - SPDR S&P 500 ETF (meistgehandelter ETF)
3. **^SPX** - S&P 500 Alternative (weniger Daten)
4. **ES=F** - E-mini S&P 500 Futures (24h Handel)

**Bestes Symbol:** ES=F hat die meisten Datenpunkte (24h Handel), aber ^GSPC ist der offizielle Index.

---

## 📁 **Generierte Dateien**

Alle Suchergebnisse wurden dokumentiert:

1. **intraday_data_search_results.json** - Vollständige Test-Ergebnisse (JSON)
2. **search_intraday_data.py** - Python-Script für die Suche
3. **INTRADAY_DATA_SEARCH_REPORT.md** - Dieser Bericht

---

## ✅ **Finales Fazit**

### **Für Ihre ursprüngliche Analyse:**

✅ **Die beste Lösung ist die bereits durchgeführte Analyse mit täglichen Daten (1990-2026):**

1. **Opening vs. Previous Close:** Vollständig analysiert mit 9,268 Tagen
2. **Wochentags-Muster:** Umfassend dokumentiert
3. **Jahrzehnt-Trends:** Klar identifiziert

**Zusätzlich verfügbar:**
- Intraday-Analyse für die letzten **2 Jahre** (erste/letzte Stunde)
- Approximation mit High/Low-Daten für alle Jahre

### **Für historische Intraday-Daten bis 1990:**

❌ **Nicht verfügbar über kostenlose APIs**

✅ **Alternativen:**
1. Kommerzielle Datenanbieter (teuer)
2. Akademischer Zugang (Universität erforderlich)
3. Approximation mit täglichen High/Low-Daten

---

**Stand:** 22. Oktober 2026  
**Tools:** Python 3.12, yfinance, pandas  
**Getestete APIs:** Yahoo Finance (primary)
