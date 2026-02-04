Historically, there have been two types of Financial Analysis; _Fundamental Analysis_ - that looks at assets, liabilities, and earnings - the cornerstone of Value Investing, and _Technical Analysis_ - that looks to look at past performance to try and predict future price movements - typically used in much shorter-term trading.

Narrative Alpha presents a third kind of analysis _"Narrative Analysis"_ that attempts to show users the "story behind their stocks," adding an element of explainability and attribution to otherwise opaque and hard to contextualise candlestick charts.

Narrative Alpha uses State-of-the-Art Topic Modeling alongside Agentic Workflows to provide users with a clear understanding of price movements along with an investment thesis.

_"To understand the economy then is to comprehend how it is driven by the animal spirits. Just as Adam Smith’s invisible hand is the keynote of classical economics, Keynes’ animal spirits are the keynote to a different view of the economy—a view that explains the underlying instabilities of capitalism."_

George Akerlof and Robert Shiller, Animal Spirits: How Human Psychology Drives the Economy, and Why It Matters for Global Capitalism, 2009.

### Key Principles

- **Evidence-First**: Every narrative summary is attributable directly to source posts and IDs
- **Balanced Analysis**: Counter-narratives are surfaced alongside supporting evidence
- **Audit Trail**: Full logging of user edits and exports
- **Trading Signals**: This tool provides context and possible buy/sell recommendations
- **Compliance-Ready**: Export client-safe memos with complete source attribution

## Use Cases

- Explain unusual price movements to clients with documented social context
- Prepare compliance documentation for investment decisions
- Research historical market events and their social media footprint
- Train junior advisors on narrative construction and source evaluation

## Tech Stack

### Frontend (`/web`)
- **Next.js 14** (App Router) with TypeScript
- **Tailwind CSS** + **shadcn/ui** components
- **Recharts** for data visualization
- **localStorage** for user edits, auditting logs and exporting history

### Backend (`/api`)
- **Python 3.11** with **FastAPI** and **Uvicorn**
- **Pydantic** for type-safe request/response models
- **CORS enabled** for local development
- **No external dependencies** (static dataset only)

## Repository Structure
```
/
├── web/                 # Next.js frontend application
├── api/                 # FastAPI backend server
├── data/
│   └── sample.json      # Static mock dataset
└── README.md
```

## Data Model

The static dataset (`/data/sample.json`) contains:

- **instruments**: Stock ticker symbols and company names
- **price_series**: Historical price and volume data
- **events**: Significant price movements with metadata (move %, volatility z-score)
- **topics**: Social media topic clusters with sentiment, keywords, and post references
- **posts**: Individual social media posts with engagement metrics

### Sample Event Structure
```json
{
  "id": "evt_001",
  "ticker": "AAPL",
  "window_start": "2024-01-15T00:00:00Z",
  "window_end": "2024-01-17T23:59:59Z",
  "move_pct": 8.5,
  "vol_z": 2.3,
  "headline": "Apple shares surge on AI partnership rumors"
}
```

### Topic Analysis
Each topic includes:
- `evidence_post_ids[]`: Posts supporting the narrative
- `counter_post_ids[]`: Posts challenging or contradicting the narrative
- `sentiment_score`: Normalized sentiment (-1 to 1)
- `share_of_posts`: Topic prevalence in the conversation

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/instruments` | List all available tickers |
| `GET` | `/ticker/{ticker}/series` | Price/volume time series |
| `GET` | `/ticker/{ticker}/events` | Significant price events |
| `GET` | `/ticker/{ticker}/event/{id}` | Full event analysis with topics and posts |
| `POST` | `/export` | Generate client-safe memo (Markdown) |

### Export Request Format
```json
{
  "ticker": "AAPL",
  "event_id": "evt_001",
  "selected_topic_ids": ["topic_1", "topic_3"],
  "edited_summary": "Custom narrative...",
  "client_safe": true
}
```

## Getting Started

### Prerequisites
- Node.js 18+ and npm/yarn
- Python 3.11+
- pip

### Installation

1. **Clone the repository**
```bash
   git clone <your-repo-url>
   cd <repo-name>
```

2. **Backend Setup**
```bash
   cd api
   pip install -r requirements.txt
   uvicorn main:app --reload --port 8000
```

3. **Frontend Setup**
```bash
   cd web
   npm install
   npm run dev
```

4. **Access the app**
   - Frontend: `http://localhost:3000`
   - API docs: `http://localhost:8000/docs`

## Features

### Evidence Transparency
- Click any narrative to view supporting posts with direct links
- See counter-arguments and contradictory evidence next to each other
- Filter topics by sentiment, prevalence or any other custom criteria

### Audit & Compliance
- Every user edit is logged with timestamp
- Export history tracked in localStorage
- Generate memos that strip internal annotations
- Markdown exports include full source attribution

### User Workflow
1. Select a ticker and date range
2. Review detected price events (volatility, magnitude, volume)
3. Explore topic clusters with evidence/counter-evidence
4. Edit and refine narrative for client presentation
5. Export compliance-ready memo with full audit trail

## Design Philosophy

This tool is **intentionally limited**:
- No live API calls or web scraping
- No algorithmic trading signals
- No predictive models or recommendations
But:
- Static datasets for reproducibility
- Human-in-the-loop narrative construction
- Full transparency on data sources

## Limitations & Disclaimers

- **Not Financial Advice**: This tool provides context, not investment recommendations.
- **Static Data Only**: No real-time feeds; datasets must be manually updated
- **Research Purposes**: Designed for internal analysis and client communication
- **No Guarantees**: Social sentiment does not predict future performance

## Contributing

Contributions welcome! Please focus on:
- Enhancing UI/UX for advisor workflows
- Improving export templates for compliance teams
- Adding data validation and error handling
- Documentation improvements

## License

MIT License - see [LICENSE](LICENSE) file for details.

This project is free and open-source software.

## Support

For questions or issues, please open a GitHub issue or contact the repository maintainer.
---

**Built for advisors who value intelligence, transparency, evidence and client trust.**
